from enum import Enum


class EquipSlot(Enum):
	A = 0
	B = 1
	C = 2
	POTION = 3


class EquipCategory(Enum):
	WEAPON = 0
	SHIELD = 1
	ARMOR = 2
	HELMET = 3
	RING = 4
	POTION = 5
