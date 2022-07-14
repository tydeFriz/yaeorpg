from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
	from models.action import Action
	from models.equip import Equip
	from models.gem import Gem
	from models.job import Job
	from models.trigger import Trigger

from collections import deque
from models.enums.attribute_enum import Attribute
from models.enums.item_enums import EquipSlot, EquipCategory
from models.enums.status_enum import Status
from helpers.status_helper import StatusHelper
from models.buff import Buff
from models.buffs.guardian_last_stand import GuardianLastStand


def _buff(new_buff: Buff, queue: deque[Buff], cap: int):
	for buff in queue:
		if buff.name == new_buff.name:
			buff.stack(new_buff.duration)
			return None

	queue.append(new_buff)
	if len(queue) > cap:
		return queue.popleft()

	return None


class Toon:

	def __init__(
			self,
			name: str,
			job: Job,
			level: int
	):
		self.name: str = name
		self.job: Job = job
		self.level: int = level
		self.attributes: dict[Attribute, int] = {
			Attribute.HP: self.job.hp_base * level,
			Attribute.TP: self.job.tp_base * level,
			Attribute.SPEED: job.speed,
			Attribute.AP: 4 * level,
			Attribute.SP: 4 * level,
			Attribute.ARMOR: 0,
			Attribute.SPELL_RES: 0,
			Attribute.STATUS_RES: 0,
			Attribute.BUFF_CAP: 3,
			Attribute.DEBUFF_CAP: 3,
			Attribute.GEM_CAP: 0,
		}
		for attribute, value in self.job.talent_attributes.items():
			self.attributes[attribute] += value

		# equip
		self._equip: dict[EquipSlot, Optional[Equip]] = {
			EquipSlot.A: None,
			EquipSlot.B: None,
			EquipSlot.C: None,
			EquipSlot.POTION: None
		}
		self.gems: list[Gem] = []

		# combat alterations
		self.hp_current: int = self.attributes[Attribute.HP]
		self.tp_current: int = self.attributes[Attribute.TP]
		self.status: Status = Status.NO_STATUS
		self.status_counter = 0
		self.buffs: deque[Buff] = deque()
		self.debuffs: deque[Buff] = deque()
		self.lingering_effects: list[Buff] = []
		self.triggers: list[Trigger] = []

	def get_available_actions(self) -> list[Action]:
		"""
		Get a list of all action the toon can take

		:return: the list of available actions
		"""
		return self.job.get_available_actions(self)

	def buff(self, new_buff: Buff) -> Optional[Buff]:
		"""
		Apply a new buff, or stack it to an already existing one

		:param new_buff: the buff to apply
		:return: the removed overflow buff, if any
		"""
		return _buff(new_buff, self.buffs, self.attributes[Attribute.BUFF_CAP])

	def debuff(self, new_debuff: Buff) -> Optional[Buff]:
		"""
		Apply a new debuff, or stack it to an already existing one

		:param new_debuff: the debuff to apply
		:return: the removed overflow debuff, if any
		"""
		return _buff(new_debuff, self.debuffs, self.attributes[Attribute.DEBUFF_CAP])

	def un_buff(self) -> Optional[Buff]:
		"""
		Removes the last applied buff

		:return: the removed buff, if any
		"""
		if self.buffs:
			return self.buffs.pop()
		return None

	def un_debuff(self) -> Optional[Buff]:
		"""
		Removes the last applied debuff

		:return: the removed debuff, if any
		"""
		if self.debuffs:
			return self.debuffs.pop()
		return None

	def damage(self, amount: int) -> bool:
		"""
		Reduce hp by a given amount

		:param amount: the amount to reduce hp_current by
		:return: True if still alive, false otherwise
		"""
		self.hp_current -= amount

		for buff in self.buffs:
			if buff.__class__ == GuardianLastStand:
				self.hp_current = 1

		if self.hp_current <= 0:
			return False
		return True

	def heal(self, amount: int) -> None:
		"""
		Increase hp by a given amount

		:param amount: the amount to increase hp_current by
		"""
		self.hp_current = min(self.hp_current + amount, self.attributes[Attribute.HP])

	def consume(self, amount: int) -> bool:
		"""
		Use the given amount of tp, if possible

		:param amount: the amount to reduce tp_current by
		:return: True if the consumption actually happened, false otherwise
		"""
		if self.tp_current < amount:
			return False

		self.tp_current = max(self.tp_current - amount, 0)
		return True

	def restore(self, amount: int) -> None:
		"""
		Increase tp by a given amount

		:param amount: the amount to increase tp_current by
		"""
		self.tp_current = min(self.tp_current + amount, self.attributes[Attribute.TP])

	def add_equip(self, item: Equip, slot: EquipSlot) -> bool:
		"""
		Set an items into a slot, replacing any previous item occupying that slot

		:param item: the item to add
		:param slot: the slot to add the item into
		:return: True if the item was correctly equipped, False otherwise
		"""
		for taken_slot, piece in self.get_equip().items():
			if taken_slot != slot and piece.category == item.category:
				return False

		if (item.category == EquipCategory.POTION and slot != EquipSlot.POTION) \
			or (item.category != EquipCategory.POTION and slot == EquipSlot.POTION):
			return False

		removed_item = self._equip[slot]
		self._equip[slot] = item

		if item.category == EquipCategory.POTION:
			return True

		if removed_item:
			self.revert_item_modifiers(removed_item)
		self.apply_item_modifiers(item)

		return True

	def remove_equip(self, slot: EquipSlot) -> Optional[Equip]:
		"""
		Remove an items from a slot

		:param slot: the slot to add the item into
		:return: the removed item, if any
		"""
		removed_item = self._equip[slot]
		self._equip[slot] = None

		if removed_item.category == EquipCategory.POTION:
			return removed_item

		if removed_item:
			self.revert_item_modifiers(removed_item)

		return removed_item

	def apply_item_modifiers(self, item: Equip) -> None:
		"""
		Apply all modifiers of an item to this Toon's stats

		:param item: the item which modifiers should be applied
		"""
		for stat in Attribute:
			self.attributes[stat] += item.modifiers[stat]

	def revert_item_modifiers(self, item: Equip) -> None:
		"""
		Remove all modifiers of an item from this Toon's stats

		:param item: the item which modifiers should be removed
		"""
		for stat in Attribute:
			self.attributes[stat] -= item.modifiers[stat]

	def get_attribute(self, attribute: Attribute) -> int:
		"""
		Get the current value of this toon's attribute

		:param attribute: the attribute to get
		:return: the current value of the attribute
		"""
		value = self.attributes[attribute]
		alterations = []
		alterations.extend(self.buffs)
		alterations.extend(self.debuffs)
		alterations.extend(StatusHelper.get_alterations_from_status(self.status))
		alterations.extend(self.lingering_effects)

		for alteration in alterations:
			for attr, mod in alteration.attribute_alterations.items():
				if attr == attribute:
					value += mod

		return value

	def get_equip(self) -> dict[EquipSlot, Equip]:
		"""
		Get all current equip as a dictionary

		:return: a dictionary of EquipSlot -> Equip entries of current equip
		"""
		result = {}

		for slot in EquipSlot:
			if self._equip[slot]:
				result[slot] = self._equip[slot]

		return result
