from dataclasses import dataclass


@dataclass
class UserProfile:
    display_name: str = "المستخدم"
    favorite_riwayah: str = "hafs"
    favorite_reader: str = ""
    memorization_goal: int = 30
    review_goal: int = 10
