import asyncio
import os
import sys
from sqlalchemy import select, func
from app.models_async.base import AsyncSessionLocal
from app.models_async.marketing import BlogPost

# Run locally
sys.path.append(os.getcwd())

async def verify_blogs():
    async with AsyncSessionLocal() as session:
        # 1. Count Total Posts
        result = await session.execute(select(func.count(BlogPost.id)))
        count = result.scalar()
        print(f"Total Blog Posts: {count}")
        
        # 2. Check Specific Series 2 Post for User Feedback content
        # Check Post 11 for EC/PPM
        stmt = select(BlogPost).where(BlogPost.slug == "science-of-water-ph-ec-ppm")
        p11 = (await session.execute(stmt)).scalars().first()
        if p11 and "Electrical Conductivity" in p11.content and "Parts Per Million" in p11.content:
            print("[✓] Post 11 contains EC vs PPM content.")
        else:
            print("[X] Post 11 Missing EC/PPM feedback!")

        # Check Post 16 for Auto Harvest Frequency
        stmt = select(BlogPost).where(BlogPost.slug == "autoflowers-vs-photoperiods-deep-dive")
        p16 = (await session.execute(stmt)).scalars().first()
        if p16 and "Perpetual Harvest" in p16.content and "4-5 Autoflower runs" in p16.content:
             print("[✓] Post 16 contains Auto Harvest Frequency content.")
        else:
            print("[X] Post 16 Missing Harvest Frequency feedback!")

        # Check Post 17 for Chemotypes
        stmt = select(BlogPost).where(BlogPost.slug == "genetics-and-phenohunting")
        p17 = (await session.execute(stmt)).scalars().first()
        if p17 and "Chemotypes" in p17.content and "Type I" in p17.content:
             print("[✓] Post 17 contains Chemotype content.")
        else:
             print("[X] Post 17 Missing Chemotype feedback!")

        # 3. Check Image Files in Static Dir
        image_dir = "app/web/static/images/blog"
        files = os.listdir(image_dir)
        print(f"Total Images in {image_dir}: {len(files)}")
        required_images = [
            "blog_ph_tester", "blog_topping_diagram", "blog_scrog_net", 
            "blog_cloning_cut", "blog_deficiency_nitrogen", "blog_autoflower_ruderallis",
            "blog_phenotypes", "blog_ventilation_diagram", "blog_dwc_bucket"
        ]
        
        missing_images = []
        for req in required_images:
            found = any(req in f for f in files)
            if not found:
                missing_images.append(req)
        
        if not missing_images:
             print("[✓] All 9 Series 2 In-Content images found in static folder.")
        else:
             print(f"[X] Missing images: {missing_images}")

if __name__ == "__main__":
    asyncio.run(verify_blogs())
