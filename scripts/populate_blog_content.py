import asyncio
import os
import sys
from datetime import datetime

# Add the project root to the python path
sys.path.append(os.getcwd())

from sqlalchemy import select
from app.models_async.base import AsyncSessionLocal
from app.models_async.marketing import BlogPost
from app.models_async.auth import User

async def populate_blogs():
    async with AsyncSessionLocal() as session:
        # 1. Get an author (Use the first admin or user found)
        result = await session.execute(select(User).limit(1))
        author = result.scalars().first()
        
        if not author:
            print("No users found. Creating default admin user...")
            author = User(
                username="admin",
                email="admin@cultivar.com",
                is_admin=True,
                is_active=True
            )
            author.set_password("admin123")
            session.add(author)
            await session.commit()
            await session.refresh(author)
            print(f"Created admin user: {author.username} (ID: {author.id})")

        print(f"Using author: {author.username} (ID: {author.id})")

        # 2. Define the posts
        posts = [
            {
                "title": "Best Ways to Germinate Seeds",
                "slug": "best-ways-to-germinate-seeds",
                "featured_image": "/static/images/blog/germinating_seeds.png",
                "excerpt": "Start your grow off right! Learn the most reliable methods for germinating cannabis seeds, from the paper towel method to direct soil planting.",
                "categories": ["Cultivation", "Beginner", "Seeds"],
                "tags": ["germination", "seeds", "seedlings", "guide"],
                "content": """
## The Miracle of Life: Starting Your Cannabis Journey

Germination is the magical moment where a dormant seed wakes up and begins its journey to becoming a lush, resin-producing plant. For many beginners, this first step can be nerve-wracking. Will it pop? Did I drown it? Is it too cold?

<div class="blog-post-image">
    <img src="/static/images/blog/blog_germination_taproot_1765026317806.png" alt="Cannabis seed germination diagram showing taproot emerging">
    <p class="image-caption">The taproot is the first sign of life. Handle with extreme care!</p>
</div>

Don't worry. Seeds are resilient, but they do have preferences. In this guide, we'll cover the most reliable methods to get close to 100% germination rates.

### What Does a Seed Need?

Before we dive into methods, let's understand what triggers germination:
1.  **Moisture**: Softens the shell and signals the embryo to wake up.
2.  **Warmth**: Spring-like temperatures (70-80°F / 21-26°C) are ideal.
3.  **Darkness**: Roots naturally grow away from light.

### Method 1: The Paper Towel Method (Classic)

This is the most popular method for a reason—it's easy to monitor.

**You'll Need:**
*   Paper towels (unbleached is best)
*   Two ceramic plates
*   Water (pH 6.0-7.0 if possible)
*   A warm spot

**Steps:**
1.  Moisten two sheets of paper towel. They should be damp, not dripping wet. Squeeze out excess water.
2.  Place one sheet on a plate.
3.  Space your seeds out on the towel.
4.  Cover with the second damp sheet.
5.  Place the second plate upside down on top to create a dark, humid dome.
6.  Check every 12-24 hours. Keep the towels moist!

**Pros:** You can see exactly when the taproot appears.
**Cons:** You must handle the delicate taproot to move it to soil.

### Method 2: Direct to Soil (Nature's Way)

This method minimizes transplant shock because you never touch the taproot.

**Steps:**
1.  Fill a small pot or solo cup with high-quality, light starting soil.
2.  Water the soil until it's moist but not soaked.
3.  Poke a hole about 0.5 to 1 inch deep (knuckle deep).
4.  Drop the seed in.
5.  Lightly cover with loose soil.
6.  Mist the surface with a spray bottle.
7.  Keep warm and wait 3-7 days.

**Pros:** No handling of delicate roots; natural.
**Cons:** You can't see what's happening; slower to sprout above ground.

### Method 3: Rapid Rooters / Jiffy Pellets

These are peat or bark plugs designed specifically for starting seeds and clones.

1.  Soak the plug in water (adjust pH to 6.3).
2.  Place the seed in the pre-made hole.
3.  Tear off a tiny piece of the plug to cover the hole lightly.
4.  Place in a humidity dome.

### Crucial Tips for Success

*   **Don't Touch the Root!** The white taproot is extremely sensitive. If you use the paper towel method, use tweezers or handle the seed by the shell, never the root.
*   **Keep it Warm:** A seedling heat mat is a great investment. Cold wet seeds will rot.
*   **Be Patient:** Some old seeds can take up to 10 days to pop.

### What's Next?

Once your seedling breaks the surface and opens its first set of rounded leaves (cotyledons), turn on your grow lights! Start with the light further away to avoid burning the baby plant, and keep the humidity high (65-70%).

Happy Growing!
"""
            },
               {
                "title": "Understanding Light Cycles: Veg vs. Flower",
                "slug": "understanding-light-cycles-veg-vs-flower",
                "featured_image": "/static/images/blog/light_cycle.png", 
                "excerpt": "Light is food for your plants. Demystify the 18/6 and 12/12 cycles and learn how to control your plant's growth stages with a simple timer.",
                "categories": ["Lighting", "Beginner", "Equipment"],
                "tags": ["lighting", "photoperiod", "veg", "flower"],
                "content": """
## Lighting the Way: The Heart of Indoor Growing

In nature, the sun dictates the life cycle of the cannabis plant. As summer turns to autumn, the days get shorter. This shift in light duration signals the plant that winter is coming, and it's time to produce flowers (buds) to reproduce.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_light_cycles_chart_1765026334242.png" alt="Chart showing 18/6 Veg cycle vs 12/12 Flower cycle">
    <p class="image-caption">Vegetative Stage (Left) vs Flowering Stage (Right). Note the increased darkness period.</p>
</div>

Indoors, we are the sun. By controlling the light cycle, we tell the plant exactly what to do.

### The Vegetative Stage (18/6)

When cannabis is young, it focuses on growing stems, leaves, and roots. This is the "Vegetative" stage. To keep a plant in this stage effectively forever (like a mother plant), we give it long days.

*   **The Schedule:** 18 hours of light, 6 hours of darkness.
*   **Why?** It mimics early summer. The plant grows rapidly and will not produce buds.
*   **Tip:** Some growers use 24 hours of light, but 18/6 saves electricity and gives the plant a rest period.

### The Flowering Stage (12/12)

This is where the magic happens. To trigger flowering in photoperiod plants, we must simulate the approach of autumn.

*   **The Schedule:** 12 hours of light, 12 hours of darkness.
*   **The Trigger:** The *uninterrupted* darkness is actually what triggers flowering. Even a small light leak during the dark period can confuse the plant and cause it to revert to veg or turn hermaphrodite.
*   **Timeline:** Most strains take 8-10 weeks after the switch to 12/12 to fully ripen.

### Auto-flowers: The Exception

Autoflowering cannabis (containing Ruderalis genetics) doesn't care about light cycles. It runs on an internal clock. You can grow autos under 18/6 or even 20/4 for their entire life.

### Choosing Your Grow Light

For beginners, LED Quantum Boards are the gold standard today. They run cooler than old HPS (High Pressure Sodium) lights and use less electricity. Look for "Full Spectrum" LEDs which provide the blue light needed for veg and the red light needed for big sticky flowers.
"""
            },
            {
                "title": "Nutrient Basics: N-P-K Explained",
                "slug": "nutrient-basics-npk-explained",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Nitrogen, Phosphorus, Potassium. Decoding the numbers on your fertilizer bottle and understanding what your plant needs.",
                "categories": ["Nutrients", "Beginner", "Science"],
                "tags": ["nutrients", "fertilizer", "feeding", "NPK"],
                "content": """
## Feeding Your Girls: What does N-P-K Mean?

Walk into any grow shop and you'll see three numbers on every bottle: 4-4-4, 2-8-4, 5-0-1. These represent the three primary macronutrients: **Nitrogen (N)**, **Phosphorus (P)**, and **Potassium (K)**.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_nutrient_bottles_1765026362029.png" alt="Fertilizer bottles showing N-P-K ratios">
    <p class="image-caption">Always check the 3 numbers on the front label. They correspond to Nitrogen, Phosphorus, and Potassium.</p>
</div>

*   **Nitrogen (N):** The "Grow" nutrient. Essential for vegetative growth, leafy green foliage, and stem structure. Deficiencies show as yellowing lower leaves.
*   **Phosphorus (P):** The "Bloom" nutrient. Vital for root development and flower production. Essential during the early bloom phase.
*   **Potassium (K):** The "Health" nutrient. Regulates water and nutrient movement in the plant. Crucial for bud density and quality.

**The Golden Rule:** Start low. It's much easier to add more nutrients than to fix a nutrient burn from overfeeding.
"""
            },
            {
                "title": "Watering 101: How to Avoid Overwatering",
                "slug": "watering-101-how-to-avoid-overwatering",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "The #1 mistake beginners make is loving their plants to death with too much water. Learn the lift method.",
                "categories": ["Cultivation", "Beginner", "Maintenance"],
                "tags": ["watering", "overwatering", "roots", "health"],
                "content": """
## Are You Drowning Your Plants?

New growers often think more water = more love. In reality, roots need **oxygen** just as much as they need water. Constant wetness suffocates roots and leads to "root rot."

<div class="blog-post-image">
    <img src="/static/images/blog/blog_watering_comparison_1765026380627.png" alt="Comparison of overwatered drooping plant vs healthy plant">
    <p class="image-caption">Left: Heavy, drooping leaves usually mean overwatering. Right: Perky leaves praying upwards indicate a healthy root zone.</p>
</div>

### The "Lift Method"
The foolproof way to water:
1.  Feel the weight of your pot when it is bone dry.
2.  Water it until runoff occurs.
3.  Feel the weight again (heavy!).
4.  **Do NOT water again** until the pot feels light again, like it did in step 1.

**Cycle:** Wet -> Dry -> Wet -> Dry. This wet/dry cycle pumps fresh oxygen into the root zone.
"""
            },
            {
                "title": "Controlling Environment: Temp & Humidity",
                "slug": "controlling-environment-temp-humidity",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "VPD, RH, and Temps. Mastering the invisible climate factors for maximum yield.",
                "categories": ["Environment", "Intermediate", "Equipment"],
                "tags": ["VPD", "temperature", "humidity", "climate"],
                "content": """
## It's Getting Hot in Here

You can have the best lights and genetics, but if your environment is off, your plants will suffer.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_hygrometer_1765026393885.png" alt="Digital Hygrometer showing ideal conditions">
    <p class="image-caption">Your hygrometer is your most important tool. Keep an eye on both Temp and RH.</p>
</div>

**Ideal Targets:**
*   **Seedling:** 75-80°F, 65-70% Humidity (RH)
*   **Veg:** 70-85°F, 40-60% RH
*   **Flower:** 65-80°F, 40-50% RH (Lower humidity prevents mold!)

**VPD (Vapor Pressure Deficit):** This is the advanced metric that combines temp and humidity to tell you how well your plant creates transpiration (sweating). Charts are available online to help you dial this in.
"""
            },
            {
                "title": "Pest Management for Beginners",
                "slug": "pest-management-for-beginners",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Spider mites, gnats, and thrips. How to spot them early and fight back organically.",
                "categories": ["IPM", "Pests", "Health"],
                "tags": ["pests", "bugs", "IPM", "prevention"],
                "content": """
## The Invaders

Pests are a reality of gardening. The key is **prevention** and **early detection**.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_pest_mites_1765026409673.png" alt="Microscope view of spider mites">
    <p class="image-caption">Spider mites are tiny but deadly. Look for small white dots on leaves and potential webbing.</p>
</div>

**The Usual Suspects:**
*   **Fungus Gnats:** Annoying little flies from wet soil. Fix: Let soil dry out, use yellow sticky traps.
*   **Spider Mites:** Tiny dots under leaves, creating webs. Very bad. Fix: Predatory mites or organic oils (neem) *in veg only*.
*   **Thrips:** Look for silver scarring on leaves.

**Prevention:** Cleanliness is godliness. Don't bring outdoor plants inside. Don't let pets in the grow room.
"""
            },
            {
                "title": "When to Harvest: Trichome Analysis",
                "slug": "when-to-harvest-trichome-analysis",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Don't chop too early! Learn to read the trichomes to harvest at peak potency.",
                "categories": ["Harvest", "Intermediate", "Quality"],
                "tags": ["harvest", "trichomes", "ripeness", "timing"],
                "content": """
## The Waiting Game

The pistils (hairs) have turned orange/brown. Is it time? Maybe, but the real truth lies in the **trichomes** (crystals).

<div class="blog-post-image">
    <img src="/static/images/blog/blog_trichome_chart_1765026432845.png" alt="Trichome maturity chart: Clear, Cloudy, Amber">
    <p class="image-caption">1. Clear (Not Ready) | 2. Cloudy (Peak THC) | 3. Amber (Sleepy/CBN). Aim for mostly cloudy!</p>
</div>

**You need a Jeweler's Loupe (30x-60x).** Look at the mushroom heads of the crystals:
1.  **Clear:** Not ready. Low potency.
2.  **Cloudy / Milky:** Peak THC. The "head high."
3.  **Amber:** Degraded THC (CBN). More "couch lock" / body effect.

**Target:** Most growers harvest when trichomes are 100% cloudy with about 10-20% amber.
"""
            },
            {
                "title": "Drying and Curing for Top Quality",
                "slug": "drying-and-curing-guide",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "The grow isn't over at harvest. Curing is the difference between hay and top-shelf bud.",
                "categories": ["Harvest", "Processing", "Quality"],
                "tags": ["drying", "curing", "harvest", "flavor"],
                "content": """
## Slow and Steady

If you dry too fast, your weed will smell like hay (chlorophyll) and taste harsh.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_drying_buds_1765026447477.png" alt="Cannabis drying in a tent">
    <p class="image-caption">Whole plant hanging at 60°F / 60% Humidity is the gold standard for preserving terpenes.</p>
</div>

**Drying:**
*   Hang whole plants upside down in a dark room.
*   Acidity: 60°F / 60% Humidity. This is the "60/60 rule."
*   Time: 10-14 days usually.
*   Test: Small branches should snap, not bend.

**Curing:**
*   Trim the buds and place in glass jars (mason jars).
*   Fill 75% full.
*   **Burp:** Open the jars for 10-15 mins daily for the first 2 weeks to let moisture escape.
*   Store in a dark cool place.
"""
            },
            {
                "title": "Choosing the Right Soil or Medium",
                "slug": "choosing-right-soil-medium",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Coco coir, living soil, or hydroponics? We break down the pros and cons for new growers.",
                "categories": ["Cultivation", "Beginner", "Setup"],
                "tags": ["soil", "coco", "hydro", "medium"],
                "content": """
## The Foundation

<div class="blog-post-image">
    <img src="/static/images/blog/blog_soil_coco_comparison_1765026460278.png" alt="Soil vs Coco Coir close up">
    <p class="image-caption">Left: Living Soil (easy, tasty). Right: Coco Coir (fast growth, more work).</p>
</div>

*   **Soil (FoxFarm, BioBizz):** Easiest for beginners. Buffers pH swings. "Living soil" requires just water.
*   **Coco Coir:** Hydroponic medium that looks like soil. Grows faster than soil but requires daily feeding and strict pH control.
*   **Deep Water Culture (DWC):** Roots sit in bubbling nutrient water. Fastest growth, but highest risk of failure if equipment breaks.

**Recommendation:** Start with high-quality organic soil. It's the most forgiving.
"""
            },
            {
                "title": "Low Stress Training (LST) Guide",
                "slug": "low-stress-training-lst-guide",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Maximize your yield by training your plants to grow wide and flat.",
                "categories": ["Techniques", "Intermediate", "Yield"],
                "tags": ["LST", "training", "yield", "canopy"],
                "content": """
## Bend it Like Beckham

Cannabis naturally grows like a Christmas tree (apical dominance). This means only the top bud gets the best light.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_lst_diagram_1765026472962.png" alt="LST Diagram showing tied down branches">
    <p class="image-caption">By tying down the main stem, you allow lower branches to catch up, creating an even canopy of top-shelf buds.</p>
</div>

**LST Goal:** Flatten the canopy so ALL buds get equal light.

**How:**
1.  Gently bend the main stem down and tie it to the side of the pot (use soft plant ties).
2.  As lower branches grow up, tie them down too.
3.  create a flat "table" of buds.

**Result:** Instead of one big cola, you get 10-20 medium/large colas.
"""
            },
            {
                "title": "The Science of Water: pH and EC/PPM",
                "slug": "science-of-water-ph-ec-ppm",
                "featured_image": "/static/images/blog/blog-default.png", 
                "excerpt": "Mastering the invisible variables. Why pH locks out nutrients and why EC is a better measurement than PPM.",
                "categories": ["Science", "Nutrients", "Intermediate"],
                "tags": ["pH", "EC", "PPM", "water chemistry"],
                "content": """
## The Invisible Variables

You can't see pH or EC with your eyes, but they are responsible for 80% of all "nutrient deficiencies." If your pH is off, your plant literally cannot access the food you are giving it.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_ph_tester_1765026924590.png" alt="Digital pH tester in water">
    <p class="image-caption">Invest in a quality pH pen. Drops and strips are too subjective for serious growers.</p>
</div>

### Understanding pH (Potential Hydrogen)

*   **Soil Range:** 6.0 - 7.0
*   **Coco/Hydro Range:** 5.5 - 6.5

If your water is too acidic (Low pH) or too alkaline (High pH), nutrients precipitate out of the solution and become "locked out."

### EC vs. PPM: What's the Difference?

This is a common source of confusion. We measure the strength of our nutrient solution to avoid burning the plants.

*   **EC (Electrical Conductivity):** This is the **pure measurement** of electricity conducted by salts in the water. It is universal and accurate.
*   **PPM (Parts Per Million):** This is a *conversion* of the EC value. The problem? There are different scales (US 500 measuring vs European 700 measuring). A reading of "1000 PPM" could mean totally different things depending on your meter's brand.

**Pro Tip:** Switch your meter to read **EC**. It is the scientific standard. Example: Seedlings like EC 0.8, Veg likes EC 1.2-1.5, and Flower likes EC 1.8-2.2.
"""
            },
            {
                "title": "Advanced Training: Topping & FIMing",
                "slug": "advanced-training-topping-fiming",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Don't be afraid to cut your plant! High Stress Training techniques to multiply your main colas.",
                "categories": ["Techniques", "Intermediate", "Yield"],
                "tags": ["topping", "FIMing", "HST", "training"],
                "content": """
## Breaking Dominance

To get a bushier plant, we must break the "Apical Dominance"—the plant's natural tendency to send all energy to the main top chute.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_topping_diagram_1765026939688.png" alt="Topping Diagram showing where to cut the stem">
    <p class="image-caption">By cutting the main tip, the two nodes below it become two new main stems.</p>
</div>

### Topping
*   **The Cut:** Cleanly snipping the main stem completely off above the 3rd, 4th, or 5th node.
*   **Result:** You get 2 main colas instead of 1.
*   **Pros:** Predictable, clean structure.

### FIMing ("Fuck I Missed")
*   **The Cut:** Pinching or cutting off 75% of the new growth tip, leaving a little bit behind.
*   **Result:** Can create 4 main colas at once.
*   **Pros:** Less stressful recovery, more tops.
*   **Cons:** Higher failure rate (sometimes it just grows back normal).
"""
            },
            {
                "title": "SCROG (Screen of Green) Masterclass",
                "slug": "scrog-screen-of-green-masterclass",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "The ultimate indoor yield technique. Weaving your canopy through a net for maximum light efficiency.",
                "categories": ["Techniques", "Advanced", "Yield"],
                "tags": ["SCROG", "trellis", "net", "canopy management"],
                "content": """
## Maximize Every Inch

Indoors, light doesn't penetrate deep. The Screen of Green (SCROG) method solves this by keeping all the buds in the "Goldilocks Zone" of perfect light intensity.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_scrog_net_1765026954614.png" alt="Cannabis canopy growing through a SCROG net">
    <p class="image-caption">A filled SCROG net ensures every square inch of your tent is producing top-shelf bud.</p>
</div>

### The Process

1.  **Install the Net:** Place a horizontal trellis net 8-12 inches above your pots.
2.  **The Vegetative Weave:** As plants grow through the holes, **tuck them back under** and move them to the next hole over. Do this until the net is 70% full.
3.  **The Flip:** Switch to 12/12 light.
4.  **The Stretch:** During the first 2 weeks of flower, the plants will stretch. Let them grow vertically through the net now.

**Result:** A solid carpet of buds with no popcorn larf at the bottom.
"""
            },
            {
                "title": "Cloning 101: Never Buy Seeds Again",
                "slug": "cloning-101-never-buy-seeds-again",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Preserve your favorite genetics forever. A step-by-step guide to taking healthy cuttings.",
                "categories": ["Propagation", "Intermediate", "Genetics"],
                "tags": ["cloning", "cuttings", "propagation", "mother plant"],
                "content": """
## The Infinite Cycle

Found a plant that smells like blueberry muffins and yields huge? Don't lose it! Clone it. A clone is an exact genetic copy of the mother.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_cloning_cut_1765026970538.png" alt="Diagram showing a 45 degree cut on a stem">
    <p class="image-caption">Cut at a 45° angle to maximize surface area for root development.</p>
</div>

### The Setup
You need a humidity dome, a sharp sterile razor, and rooting hormone (gel or powder).

### The Steps
1.  **Select a Branch:** Choose a healthy lower branch with 3-4 nodes.
2.  **The Cut:** Slice cleanly at a 45-degree angle just below a node.
3.  **The Dip:** Immediately dip the cut end into rooting gel.
4.  **The Plug:** Place gently into a Rapid Rooter or Rockwool cube.
5.  **The Dome:** Mist the leaves and place in the dome. Close the vents for 3 days to keep humidity at 100%.

**Success:** In 7-14 days, you should see white roots poking out.
"""
            },
            {
                "title": "Doctor's Office: Diagnosing Deficiencies",
                "slug": "doctors-office-diagnosing-deficiencies",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Yellow leaves? Brown spots? Diagnosing common nutrient issues before they kill your crop.",
                "categories": ["Troubleshooting", "Health", "Intermediate"],
                "tags": ["deficiencies", "sick plant", "diagnosis", "nitrogen"],
                "content": """
## Reading the Leaves

Your plant talks to you through its leaves. The location of the problem tells you half the story.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_deficiency_nitrogen_1765026995111.png" alt="Nitrogen deficiency showing yellow bottom leaves">
    <p class="image-caption">Nitrogen is a "Mobile" nutrient. The plant steals it from old bottom leaves to feed new top growth, causing yellowing at the bottom.</p>
</div>

### Mobile vs Immobile Nutrients

*   **Mobile (N, P, K, Mg):** Problems start at the **bottom** of the plant. The plant moves these nutrients to the top.
    *   *Example:* Nitrogen deficiency = Yellow bottom leaves.
*   **Immobile (Ca, Fe, S):** Problems start at the **top** of the plant. The plant cannot move these.
    *   *Example:* Calcium deficiency = Rust spots on new top leaves.

**First Step:** Always check pH before adding more food. Bad pH looks like a deficiency!
"""
            },
            {
                "title": "Deep Dive: Autoflowers vs Photoperiods",
                "slug": "autoflowers-vs-photoperiods-deep-dive",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Speed vs Size. Why modern autos are changing the game and how to choose the right type for you.",
                "categories": ["Genetics", "Beginner", "Planning"],
                "tags": ["autoflower", "photoperiod", "ruderalis", "harvest"],
                "content": """
## The Ruderalis Revolution

Ten years ago, "Autos" were tiny and weak. Today, they rival photoperiods in potency.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_autoflower_ruderallis_1765027009696.png" alt="Small stout Ruderalis plant">
    <p class="image-caption">Autos stay smaller and bushier, making them perfect for closet grows.</p>
</div>

### The Speed Advantage (Perpetual Harvest)

The biggest advantage of Autoflowers is speed. Most go from seed to harvest in 70-80 days.
*   **Photoperiods:** Require 4-5 months minimum.
*   **The Math:** You can fit **4-5 Autoflower runs** in a single year, versus only **2-3 Photoperiod runs**. If you want constant fresh harvests, Autos are the king of throughput.

### Why Choose Photoperiods?
1.  **Control:** You decide when they flower.
2.  **Forgiveness:** If you make a mistake in veg, you can just wait an extra week to let it recover before flipping to flower. With Autos, the clock is ticking and mistakes directly reduce yield.
3.  **Cloning:** You generally cannot clone Autos efficiently.
"""
            },
            {
                "title": "Genetics & Phenohunting",
                "slug": "genetics-and-phenohunting",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Why do two seeds from the same pack look different? Learn about genotypes, phenotypes, and chemotypes.",
                "categories": ["Genetics", "Advanced", "Breeding"],
                "tags": ["phenotype", "genotype", "chemotype", "breeding"],
                "content": """
## The Hunt for the Keeper

You pop 10 seeds of "Blue Dream." One is tall and lanky, one is short and bushy, one turns purple. Why?

<div class="blog-post-image">
    <img src="/static/images/blog/blog_phenotypes_1765027023866.png" alt="Two different phenotypes side by side">
    <p class="image-caption">Same parents, different kids. This natural variation is called "Phenotypic Variation."</p>
</div>

*   **Genotype:** The genetic code (the potential).
*   **Phenotype:** The physical expression of that code in your specific environment.

### Chemotypes: It's Not Just THC

Beyond looks, plants have different chemical profiles, or "Chemotypes."
*   **Type I:** High THC, Low CBD (Most modern recreational strains).
*   **Type II:** Mixed Ratio (1:1 THC:CBD). Great for medical users.
*   **Type III:** High CBD, Low THC (Hemp compliance).

**Phenohunting:** The process of popping many seeds to find that one "Unicorn" phenotype that has the perfect smell, color, and high—and then cloning it to keep it forever.
"""
            },
            {
                "title": "The Invisible Garden: Ventilation & Odor Control",
                "slug": "ventilation-and-odor-control",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Don't let the smell give you away. Setting up proper negative pressure and airflow.",
                "categories": ["Environment", "Setup", "Equipment"],
                "tags": ["ventilation", "carbon filter", "airflow", "smell"],
                "content": """
## Fresh Air In, Stale Air Out

Plants breathe CO2. If you don't exchange the air in your tent, growth stalls. And in flower, your house will smell like a skunks convention without a filter.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_ventilation_diagram_1765027036739.png" alt="Diagram of airflow in a grow tent">
    <p class="image-caption">Negative Pressure: The exhaust fan sucks air OUT, pulling fresh air IN through the passive vents at the bottom.</p>
</div>

### The Setup
1.  **Carbon Filter:** Scrub the smell. Hang this at the very top of your tent (heat rises).
2.  **Inline Fan:** Sucks air through the filter and blows it outside the tent.
3.  **Negative Pressure:** Your tent walls should suck *inwards* slightly. This ensures no smell escapes through the zippers.

**CFM Rule:** Buy a fan that can exchange all the air in your tent once per minute.
"""
            },
            {
                "title": "Intro to Hydroponics: DWC (Deep Water Culture)",
                "slug": "intro-to-hydroponics-dwc",
                "featured_image": "/static/images/blog/blog-default.png",
                "excerpt": "Explosive growth rates with Deep Water Culture. A guide to the bucket system.",
                "categories": ["Hydroponics", "Advanced", "Techniques"],
                "tags": ["DWC", "hydroponics", "roots", "buckets"],
                "content": """
## The Formula 1 of Growing

Deep Water Culture (DWC) is the simplest form of true hydroponics. No soil, no coco—just water, bubbles, and nutrients.

<div class="blog-post-image">
    <img src="/static/images/blog/blog_dwc_bucket_1765027051412.png" alt="Cross section of a DWC Bucket">
    <p class="image-caption">Roots hang directly into the oxygenated nutrient solution. This unlimited access leads to massive growth spurts.</p>
</div>

### How it Works
*   The plant sits in a "Net Pot" filled with clay pebbles (Hydroton).
*   The roots dangle below into a bucket of water.
*   **The Secret:** An air stone pumped by an air pump sits at the bottom, turning the water into a fizzy "root jacuzzi."

### Pros & Cons
*   **Pros:** 2x faster vegetative growth than soil. Huge yields.
*   **Cons:** If your water gets hot (>72°F), root rot kills plants overnight. If the pump fails, plants die in hours. It is high risk, high reward.
"""
            }
        ]

        for post_data in posts:
            cats = post_data.pop("categories", [])
            tag_list = post_data.pop("tags", [])
            
            # Check if exists
            stmt = select(BlogPost).where(BlogPost.slug == post_data["slug"])
            result = await session.execute(stmt)
            existing_post = result.scalars().first()

            if existing_post:
                print(f"Updating post: {post_data['title']}")
                for k, v in post_data.items():
                    setattr(existing_post, k, v)
                existing_post.categories = cats
                existing_post.tags = tag_list
                # Make sure it's published
                existing_post.is_published = True
                existing_post.published_at = datetime.utcnow()
            else:
                print(f"Creating post: {post_data['title']}")
                new_post = BlogPost(
                    **post_data,
                    categories=cats,
                    tags=tag_list,
                    author_id=author.id,
                    is_published=True,
                    published_at=datetime.utcnow()
                )
                session.add(new_post)
        
        await session.commit()
        print("Done!")

if __name__ == "__main__":
    asyncio.run(populate_blogs())
