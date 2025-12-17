import random
from pathlib import Path
from datetime import time as dtime

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from base.models import (
    Restaurant,
    Genre,
    SpotSubArea,
    Ward,
    OpeningHour,
)


class Command(BaseCommand):
    help = "Dummyのレストランデータを生成してDBに投入する"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=10,
            help="生成するレストラン件数（デフォルト10件）",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker("ja_JP")
        total = options["total"]

        genres = list(Genre.objects.all())
        sub_areas = list(SpotSubArea.objects.select_related("spot"))
        if not genres or not sub_areas:
            self.stdout.write(
                self.style.ERROR(
                    "Genre と SpotSubArea を先にマスタ登録してから実行して。"
                )
            )
            return

        dummy_path = settings.MEDIA_ROOT / "restaurant_images" / "dummy.png"

        self.stdout.write(self.style.WARNING(f"{total}件のレストランを生成します…"))

        for _ in range(total):
            sub_area = random.choice(sub_areas)
            ward_value = sub_area.ward


            main_genre = random.choice(genres)
            owner_name = fake.last_name()
            suffix = random.choice(["本店", "総本家", ""])

            name = f"{main_genre.name} {owner_name}屋 {suffix}"
            
            templates = [
                "地元の味を気軽に楽しめる一軒として親しまれています。",
                "落ち着いた空間で名古屋の味を堪能いただけます。",
                "観光客にも地元客にも愛される味を提供しています。",
            ]

            description = (
                f"{main_genre.name}を看板メニューにした名古屋めし専門店です。" + random.choice(templates)
            )

            ban = random.randint(1, 20)
            go = random.randint(1, 30)
            address_tail = f"{ban}-{go}"

            phone = phone = f"000-{random.randint(1000,9999)}-{random.randint(1000,9999)}"

            min_party = 1
            max_party = random.choice([4, 6])

            restaurant = Restaurant.objects.create(
                name=name,
                description=description,
                ward=ward_value,
                sub_area=sub_area,
                address=address_tail,
                phone_number=phone,
                min_party_size=min_party,
                max_party_size=max_party,
            )

            if dummy_path.exists():
                with dummy_path.open("rb") as f:
                    restaurant.image.save(dummy_path.name, File(f), save=True)

            k = random.randint(1, min(3, len(genres)))
            chosen_genres = random.sample(genres, k=k)
            if main_genre not in chosen_genres:
                chosen_genres[0] = main_genre
            restaurant.genre.set(chosen_genres)

            holiday_count = random.randint(0, 2)

            holidays = random.sample(list(OpeningHour.Weekday.values), k=holiday_count)

            for weekday_value in OpeningHour.Weekday.values:
                if weekday_value in holidays:
                    continue

                OpeningHour.objects.create(
                    restaurant=restaurant,
                    weekday=weekday_value,
                    open_time=dtime(hour=11, minute=0),
                    close_time=dtime(hour=15, minute=0),
                )
                OpeningHour.objects.create(
                    restaurant=restaurant,
                    weekday=weekday_value,
                    open_time=dtime(hour=17, minute=0),
                    close_time=dtime(hour=22, minute=0),
                )

        self.stdout.write(
            self.style.SUCCESS(f"Dummyレストラン {total}件の作成が完了しました。")
        )
