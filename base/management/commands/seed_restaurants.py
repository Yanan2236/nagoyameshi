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

        # 1枚だけ用意して全店舗で使い回す画像
        dummy_path = settings.MEDIA_ROOT / "restaurant_images" / "dummy.png"

        self.stdout.write(self.style.WARNING(f"{total}件のレストランを生成します…"))

        for _ in range(total):
            sub_area = random.choice(sub_areas)

            # Restaurant.ward は SubArea に合わせる
            ward_value = sub_area.ward

            # メインジャンルを1つ決めて店名に混ぜる
            main_genre = random.choice(genres)
            owner_name = fake.last_name()  # 例: 山田
            suffix = random.choice(["本店", "総本家", ""])
            # 例: 「ひつまぶし 山田屋 本店」
            name = f"{main_genre.name} {owner_name}屋 {suffix}"
            
            templates = [
                "地元の味を気軽に楽しめる一軒として親しまれています。",
                "落ち着いた空間で名古屋の味を堪能いただけます。",
                "観光客にも地元客にも愛される味を提供しています。",
            ]

            description = (
                f"{main_genre.name}を看板メニューにした名古屋めし専門店です。" + random.choice(templates)
            )

            # 住所の構造：
            #  - Ward: 区名（フィールド ward）
            #  - SubArea.name: 町名・丁目の頭
            #  - address: 残り（○丁目△-□ だけ入れる）
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

            # 画像：1枚あれば全店舗同じ画像を付ける
            if dummy_path.exists():
                with dummy_path.open("rb") as f:
                    restaurant.image.save(dummy_path.name, File(f), save=True)

            # ジャンルは 1〜3 個ランダムに付与（店名に使ったジャンルも含める）
            k = random.randint(1, min(3, len(genres)))
            chosen_genres = random.sample(genres, k=k)
            if main_genre not in chosen_genres:
                chosen_genres[0] = main_genre
            restaurant.genre.set(chosen_genres)

            # 営業時間：全曜日 11–15, 17–22 の二部制をとりあえず入れておく
            # 休みの数をランダム選択（0〜2日）
            holiday_count = random.randint(0, 2)

            # Weekday.values は ['mon','tue',...]
            # 重複なしで休日を抽出
            holidays = random.sample(list(OpeningHour.Weekday.values), k=holiday_count)

            for weekday_value in OpeningHour.Weekday.values:
                # 休日ならスキップ
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
