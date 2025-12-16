import time
import difflib
from typing import List, Dict, Any

import pandas as pd
import streamlit as st


# -----------------------------
# Page & Theme Configuration
# -----------------------------
st.set_page_config(
    page_title="Smart Gift Recommender",
    page_icon="🎁",
    layout="wide",
)


# -----------------------------
# Styling & Intro Animation
# -----------------------------
def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        /* Global background */
        .stApp {
            background: radial-gradient(circle at top left, #fdfbfb 0%, #ebedee 35%, #f5f7fa 70%, #c3cfe2 100%);
            font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Card-like containers */
        .gift-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 18px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.10);
            border: 1px solid rgba(148, 163, 184, 0.35);
            backdrop-filter: blur(6px);
        }

        .gift-title {
            font-weight: 700;
            font-size: 1.05rem;
            margin-bottom: 0.35rem;
        }

        .gift-meta {
            font-size: 0.85rem;
            color: #64748b;
            margin-bottom: 0.35rem;
        }

        .gift-why {
            font-size: 0.9rem;
            color: #0f172a;
        }

        .gift-price {
            font-weight: 600;
            color: #16a34a;
        }

        /* Buy button style */
        .gift-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.45rem 0.9rem;
            border-radius: 999px;
            border: none;
            font-size: 0.85rem;
            font-weight: 600;
            color: white !important;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            text-decoration: none !important;
            box-shadow: 0 8px 15px rgba(79, 70, 229, 0.35);
            transition: transform 0.08s ease-out, box-shadow 0.12s ease-out, filter 0.15s ease-out;
        }

        .gift-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 12px 28px rgba(79, 70, 229, 0.45);
            filter: brightness(1.03);
        }

        /* Intro animated headline */
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.2rem 0.75rem;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.06);
            border: 1px solid rgba(148, 163, 184, 0.45);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #475569;
            margin-bottom: 0.3rem;
        }

        .hero-gradient-text {
            background: radial-gradient(circle at 0% 0%, #f97316, #ec4899 25%, #6366f1 55%, #22c55e 80%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: hue-shift 12s linear infinite;
        }

        @keyframes hue-shift {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }

        /* Mobile tweaks */
        @media (max-width: 768px) {
            .gift-card {
                padding: 0.9rem 1rem;
            }
            .gift-title {
                font-size: 0.98rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def run_intro_animation() -> None:
    placeholder = st.empty()
    with placeholder.container():
        cols = st.columns([1, 2, 1])
        with cols[1]:
            st.markdown(
                """
                <div style="text-align: center; margin-top: 1.2rem;">
                    <div class="hero-badge">
                        <span>✨ Smart Matching</span>
                        <span>·</span>
                        <span>Powered by vibes & data</span>
                    </div>
                    <h1 class="hero-gradient-text" style="font-size: 2.2rem; margin-bottom: 0.25rem;">
                        Smart Gift Recommender
                    </h1>
                    <p style="font-size: 0.97rem; color: #475569; max-width: 26rem; margin: 0 auto;">
                        Tell us who you're shopping for — we’ll translate their hobbies, profession, and online obsessions into spot‑on gift ideas.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            progress = st.progress(0, text="Tuning into their personality...")
            for i in range(0, 101, 10):
                time.sleep(0.07)
                progress.progress(i, text="Finding thoughtful surprises..." if i > 50 else "Tuning into their personality...")

    time.sleep(0.2)
    placeholder.empty()
    st.balloons()


# -----------------------------
# Gift Dataset
# -----------------------------
def build_gift_dataset() -> pd.DataFrame:
    # NOTE: price ranges & links are placeholders; image URLs use freely usable Unsplash photos.
    gifts: List[Dict[str, Any]] = [
        {
            "name": "Noise-Cancelling Headphones",
            "min_age": 16,
            "max_age": 60,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Doctor", "Artist"],
            "hobby_tags": ["Music", "Travel", "Gaming", "Reading"],
            "social_tags": ["productivity", "focus", "study-with-me", "music"],
            "social_trend_score": 9.2,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1519659528534-9e3f76e6f2c8?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=noise+cancelling+headphones",
            "why_base": "Blocks out distractions and makes every playlist, podcast, or focus session feel premium.",
        },
        {
            "name": "Smart Fitness Band",
            "min_age": 14,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Doctor", "Teacher"],
            "hobby_tags": ["Sports", "Travel"],
            "social_tags": ["fitness", "steps", "health-tracking", "gym"],
            "social_trend_score": 8.9,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=fitness+band",
            "why_base": "Perfect for anyone into health or movement, with gentle nudges to stay active.",
        },
        {
            "name": "Kindle E‑reader",
            "min_age": 15,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Student", "Teacher", "Doctor", "Engineer"],
            "hobby_tags": ["Reading", "Travel"],
            "social_tags": ["booktok", "reading", "minimalism"],
            "social_trend_score": 9.4,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=kindle",
            "why_base": "Turns any spare moment into reading time, without carrying heavy books.",
        },
        {
            "name": "Gourmet Coffee Sampler",
            "min_age": 18,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Engineer", "Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Cooking", "Reading"],
            "social_tags": ["coffee", "aesthetic-mornings"],
            "social_trend_score": 7.8,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=gourmet+coffee+sampler",
            "why_base": "For the person who treats their morning coffee like a mini ritual.",
        },
        {
            "name": "Custom Sketch Portrait",
            "min_age": 10,
            "max_age": 80,
            "gender_pref": "Any",
            "profession_match": ["Artist", "Teacher", "Student"],
            "hobby_tags": ["Art", "Photography", "Travel"],
            "social_tags": ["aesthetic", "memories", "home-decor"],
            "social_trend_score": 8.3,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.etsy.com/search?q=custom+portrait",
            "why_base": "Deeply personal and decor‑friendly, this turns a favorite photo into art.",
        },
        {
            "name": "Desk Plant Set",
            "min_age": 16,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Engineer", "Doctor", "Teacher", "Artist", "Student"],
            "hobby_tags": ["Gardening", "Reading"],
            "social_tags": ["desk-setup", "aesthetic", "plant-parent"],
            "social_trend_score": 7.5,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=desk+plant",
            "why_base": "Adds a calm, green vibe to any workspace and is easy to care for.",
        },
        {
            "name": "Streaming Service Gift Card",
            "min_age": 13,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Teacher", "Artist", "Doctor"],
            "hobby_tags": ["Movies", "Gaming", "Music"],
            "social_tags": ["binge-watch", "movies", "series"],
            "social_trend_score": 8.1,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1594904351111-7bcd590d0186?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=streaming+gift+card",
            "why_base": "Lets them pick exactly what they want to binge or listen to next.",
        },
        {
            "name": "Ergonomic Gaming Mouse",
            "min_age": 13,
            "max_age": 40,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer"],
            "hobby_tags": ["Gaming", "Design"],
            "social_tags": ["gaming-setup", "rgb"],
            "social_trend_score": 8.7,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1587202372775-98973d4a18bd?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=gaming+mouse",
            "why_base": "Great for marathon gaming sessions or precision‑heavy computer work.",
        },
        {
            "name": "Mechanical Keyboard",
            "min_age": 16,
            "max_age": 50,
            "gender_pref": "Any",
            "profession_match": ["Engineer", "Student", "Artist"],
            "hobby_tags": ["Gaming", "Writing"],
            "social_tags": ["keyboard-asmr", "desk-setup"],
            "social_trend_score": 9.0,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1514996937319-344454492b37?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=mechanical+keyboard",
            "why_base": "A satisfying, aesthetic upgrade for anyone who types or games a lot.",
        },
        {
            "name": "Instant Camera",
            "min_age": 12,
            "max_age": 40,
            "gender_pref": "Any",
            "profession_match": ["Student", "Artist"],
            "hobby_tags": ["Travel", "Photography"],
            "social_tags": ["travel-vlog", "film-camera"],
            "social_trend_score": 8.8,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1516031190212-da133013de50?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=instant+camera",
            "why_base": "Instant prints turn hangouts and trips into tangible keepsakes.",
        },
        {
            "name": "Travel Backpack with USB Port",
            "min_age": 15,
            "max_age": 60,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Doctor", "Teacher"],
            "hobby_tags": ["Travel"],
            "social_tags": ["airport-outfit", "digital-nomad"],
            "social_trend_score": 7.9,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1500534314211-0a24cd03f2c0?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=travel+backpack+usb",
            "why_base": "Keeps gadgets charged and essentials organized on the go.",
        },
        {
            "name": "Cozy Weighted Blanket",
            "min_age": 16,
            "max_age": 80,
            "gender_pref": "Any",
            "profession_match": ["Engineer", "Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Reading", "Movies"],
            "social_tags": ["self-care", "sleep", "cozy"],
            "social_trend_score": 8.4,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1519710884009-22a6914861f2?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=weighted+blanket",
            "why_base": "Great for winding down, movie nights, or anyone who loves cozy vibes.",
        },
        {
            "name": "Minimalist Notebook Set",
            "min_age": 12,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Student", "Teacher", "Engineer", "Doctor", "Artist"],
            "hobby_tags": ["Writing", "Reading"],
            "social_tags": ["bullet-journal", "studygram"],
            "social_trend_score": 7.6,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=minimalist+notebook",
            "why_base": "Perfect for ideas, notes, sketches, or planning out their next big thing.",
        },
        {
            "name": "Premium Fountain Pen",
            "min_age": 18,
            "max_age": 75,
            "gender_pref": "Any",
            "profession_match": ["Doctor", "Teacher", "Engineer", "Artist"],
            "hobby_tags": ["Writing", "Art"],
            "social_tags": ["calligraphy", "journaling"],
            "social_trend_score": 7.3,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=fountain+pen",
            "why_base": "Turns everyday notes and signatures into a small luxury moment.",
        },
        {
            "name": "Art Supply Starter Kit",
            "min_age": 10,
            "max_age": 40,
            "gender_pref": "Any",
            "profession_match": ["Student", "Artist"],
            "hobby_tags": ["Art", "DIY"],
            "social_tags": ["art-tiktok", "sketchbook-tour"],
            "social_trend_score": 8.0,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=art+supply+set",
            "why_base": "Encourages creativity and makes it easy to dive into drawing or painting.",
        },
        {
            "name": "Professional Chef Knife",
            "min_age": 18,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Cooking"],
            "social_tags": ["cooking-reels", "meal-prep"],
            "social_trend_score": 8.2,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=chef+knife",
            "why_base": "Elevates everyday cooking and feels like a pro‑level upgrade in the kitchen.",
        },
        {
            "name": "Cooking Class Voucher",
            "min_age": 18,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Doctor", "Teacher", "Engineer", "Artist"],
            "hobby_tags": ["Cooking", "Travel"],
            "social_tags": ["date-idea", "experience-gift"],
            "social_trend_score": 7.9,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.airbnb.com/s/cooking-class",
            "why_base": "Ideal for food lovers who enjoy learning by doing and creating memories.",
        },
        {
            "name": "Language Learning App Subscription",
            "min_age": 13,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Teacher", "Artist"],
            "hobby_tags": ["Travel", "Reading"],
            "social_tags": ["self-improvement", "productivity"],
            "social_trend_score": 7.7,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1523580846011-d3a5bc25702b?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.duolingo.com/",
            "why_base": "Great for curious minds and frequent travelers picking up new languages.",
        },
        {
            "name": "Portable Bluetooth Speaker",
            "min_age": 12,
            "max_age": 60,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Artist", "Teacher"],
            "hobby_tags": ["Music", "Travel", "Sports"],
            "social_tags": ["beach-day", "picnic", "room-decor"],
            "social_trend_score": 8.5,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1519677100203-a0e668c92439?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=bluetooth+speaker",
            "why_base": "Brings music, podcasts, and parties wherever they go.",
        },
        {
            "name": "Yoga Mat & Block Set",
            "min_age": 14,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Sports", "Fitness"],
            "social_tags": ["wellness", "yoga", "pilates"],
            "social_trend_score": 8.3,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1603988363607-41a96cdcd875?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=yoga+mat+set",
            "why_base": "Perfect for at‑home workouts, stretching, or calm morning routines.",
        },
        {
            "name": "Smart LED Strip Lights",
            "min_age": 10,
            "max_age": 35,
            "gender_pref": "Any",
            "profession_match": ["Student", "Artist"],
            "hobby_tags": ["Gaming", "Music"],
            "social_tags": ["room-makeover", "rgb"],
            "social_trend_score": 9.1,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1505740106531-4243f3831c78?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=led+strip+lights",
            "why_base": "Transforms any room into a cozy, colorful, TikTok‑ready space.",
        },
        {
            "name": "Board Game Night Bundle",
            "min_age": 12,
            "max_age": 60,
            "gender_pref": "Any",
            "profession_match": ["Teacher", "Engineer", "Artist"],
            "hobby_tags": ["Gaming"],
            "social_tags": ["game-night", "friends"],
            "social_trend_score": 7.4,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=board+game+bundle",
            "why_base": "Great for social butterflies who love hosting or hanging out with friends.",
        },
        {
            "name": "Smart Mug Warmer",
            "min_age": 18,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Engineer", "Teacher", "Doctor", "Artist"],
            "hobby_tags": ["Reading", "Work"],
            "social_tags": ["desk-setup", "coffee"],
            "social_trend_score": 7.2,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=mug+warmer",
            "why_base": "Ideal for long focus sessions where coffee always gets cold too fast.",
        },
        {
            "name": "Coding Course Voucher",
            "min_age": 14,
            "max_age": 45,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer"],
            "hobby_tags": ["Gaming", "Tech"],
            "social_tags": ["tech-gadgets", "career-growth"],
            "social_trend_score": 8.6,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.udemy.com/courses/search/?q=coding",
            "why_base": "A future‑focused gift for anyone curious about programming or tech.",
        },
        {
            "name": "3D Printing Pen",
            "min_age": 10,
            "max_age": 35,
            "gender_pref": "Any",
            "profession_match": ["Student", "Artist"],
            "hobby_tags": ["Art", "DIY", "Tech"],
            "social_tags": ["diy-projects", "crafts"],
            "social_trend_score": 7.9,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1581090700227-1e37b190418e?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=3d+printing+pen",
            "why_base": "Blends creativity and technology for fun 3D doodles and mini projects.",
        },
        {
            "name": "Virtual Reality Headset",
            "min_age": 13,
            "max_age": 40,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer"],
            "hobby_tags": ["Gaming", "Tech"],
            "social_tags": ["vr-gaming", "metaverse"],
            "social_trend_score": 9.3,
            "price_range": "$$$",
            "image_url": "https://images.unsplash.com/photo-1587613864521-9ef8dfe617cc?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=vr+headset",
            "why_base": "Immersive experiences for gamers and tech enthusiasts alike.",
        },
        {
            "name": "Fashion Sneaker Gift Card",
            "min_age": 14,
            "max_age": 40,
            "gender_pref": "Any",
            "profession_match": ["Student", "Artist"],
            "hobby_tags": ["Sports", "Fashion"],
            "social_tags": ["streetwear", "outfit-inspo"],
            "social_trend_score": 8.4,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.nike.com/gift-cards",
            "why_base": "Lets them pick sneakers that match their exact vibe and style.",
        },
        {
            "name": "Ring Light with Tripod",
            "min_age": 13,
            "max_age": 40,
            "gender_pref": "Any",
            "profession_match": ["Student", "Artist", "Teacher"],
            "hobby_tags": ["Content Creation", "Photography"],
            "social_tags": ["reels", "tiktok", "youtube"],
            "social_trend_score": 9.0,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1618004912476-29818d81ae2e?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=ring+light+tripod",
            "why_base": "Perfect for someone posting reels, tutorials, or video calls.",
        },
        {
            "name": "Desktop Cable Organizer",
            "min_age": 16,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Engineer", "Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Tech"],
            "social_tags": ["desk-setup", "minimalism"],
            "social_trend_score": 7.0,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1512427691650-1e0c2f9a81b3?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=cable+organizer+desk",
            "why_base": "Great for tidy minds who love clean, clutter‑free setups.",
        },
        {
            "name": "Portable Projector",
            "min_age": 16,
            "max_age": 60,
            "gender_pref": "Any",
            "profession_match": ["Student", "Teacher", "Artist"],
            "hobby_tags": ["Movies", "Gaming"],
            "social_tags": ["movie-night", "backyard"],
            "social_trend_score": 8.6,
            "price_range": "$$$",
            "image_url": "https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=mini+projector",
            "why_base": "Turns any wall into a cinema for movies, games, or big‑screen slides.",
        },
        {
            "name": "Stylish Laptop Sleeve",
            "min_age": 15,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Travel", "Tech"],
            "social_tags": ["office-aesthetic", "digital-nomad"],
            "social_trend_score": 7.8,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1516387938699-a93567ec168e?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=laptop+sleeve",
            "why_base": "Blends protection and style for laptops carried everywhere.",
        },
        {
            "name": "Barista Milk Frother",
            "min_age": 18,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Doctor", "Teacher", "Engineer", "Artist"],
            "hobby_tags": ["Cooking"],
            "social_tags": ["coffee", "home-cafe"],
            "social_trend_score": 7.5,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=milk+frother",
            "why_base": "For the latte lover building a cozy café right at home.",
        },
        {
            "name": "Minimalist Wall Art Print Set",
            "min_age": 16,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Artist", "Student", "Teacher"],
            "hobby_tags": ["Art", "Interior Design"],
            "social_tags": ["room-decor", "aesthetic"],
            "social_trend_score": 7.9,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1523755231516-e43fd2e8dca5?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.etsy.com/search?q=minimalist+wall+art",
            "why_base": "Elevates their room with art that matches modern, clean aesthetics.",
        },
        {
            "name": "Smart Notebook (Reusable)",
            "min_age": 15,
            "max_age": 50,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Teacher", "Artist"],
            "hobby_tags": ["Writing", "Tech"],
            "social_tags": ["productivity", "note-taking"],
            "social_trend_score": 8.1,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=smart+reusable+notebook",
            "why_base": "Great for eco‑conscious note takers who love writing by hand.",
        },
        {
            "name": "Portable Power Bank",
            "min_age": 12,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Travel", "Tech", "Gaming"],
            "social_tags": ["travel-essentials", "always-online"],
            "social_trend_score": 8.0,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=power+bank",
            "why_base": "Ideal for people who hate seeing their battery drop under 20%.",
        },
        {
            "name": "Digital Drawing Tablet",
            "min_age": 12,
            "max_age": 40,
            "gender_pref": "Any",
            "profession_match": ["Student", "Artist"],
            "hobby_tags": ["Art", "Design"],
            "social_tags": ["digital-art", "procreate"],
            "social_trend_score": 8.9,
            "price_range": "$$$",
            "image_url": "https://images.unsplash.com/photo-1526498460520-4c246339dccb?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=drawing+tablet",
            "why_base": "Perfect for aspiring illustrators and designers exploring digital art.",
        },
        {
            "name": "Running Shoes Gift Card",
            "min_age": 16,
            "max_age": 55,
            "gender_pref": "Any",
            "profession_match": ["Doctor", "Engineer", "Teacher"],
            "hobby_tags": ["Sports", "Fitness"],
            "social_tags": ["running", "fitness-reels"],
            "social_trend_score": 8.2,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1526403224631-0604b82829a1?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.adidas.com/us/giftcards",
            "why_base": "Lets them choose gear that matches their workout style and goals.",
        },
        {
            "name": "Scented Candle Set",
            "min_age": 16,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Artist", "Teacher", "Doctor", "Engineer"],
            "hobby_tags": ["Reading", "Self-care"],
            "social_tags": ["cozy", "room-decor"],
            "social_trend_score": 7.4,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1511910849309-0dffb8785145?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=scented+candle+set",
            "why_base": "Great for relaxing evenings, baths, or cozy reading corners.",
        },
        {
            "name": "Premium Sketchbook",
            "min_age": 10,
            "max_age": 60,
            "gender_pref": "Any",
            "profession_match": ["Artist", "Student"],
            "hobby_tags": ["Art"],
            "social_tags": ["sketchbook-tour", "art-tiktok"],
            "social_trend_score": 7.8,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1526498460520-4c246339dccb?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=artist+sketchbook",
            "why_base": "A blank canvas for doodles, studies, and big creative ideas.",
        },
        {
            "name": "Photography Masterclass",
            "min_age": 16,
            "max_age": 55,
            "gender_pref": "Any",
            "profession_match": ["Artist", "Student", "Teacher"],
            "hobby_tags": ["Photography", "Travel"],
            "social_tags": ["photo-tutorials", "content-creation"],
            "social_trend_score": 8.1,
            "price_range": "$$$",
            "image_url": "https://images.unsplash.com/photo-1452587925148-ce544e77e70d?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.masterclass.com/classes",
            "why_base": "For the friend whose camera roll is already museum‑level.",
        },
        {
            "name": "Gourmet Snack Box Subscription",
            "min_age": 14,
            "max_age": 60,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Teacher", "Doctor", "Artist"],
            "hobby_tags": ["Cooking", "Movies"],
            "social_tags": ["snack-haul", "unboxing"],
            "social_trend_score": 8.0,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=snack+box+subscription",
            "why_base": "A monthly surprise of treats from around the world or themed boxes.",
        },
        {
            "name": "Standing Desk Converter",
            "min_age": 20,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Engineer", "Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Work", "Tech"],
            "social_tags": ["productivity", "home-office"],
            "social_trend_score": 7.9,
            "price_range": "$$$",
            "image_url": "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=standing+desk+converter",
            "why_base": "Supports better posture and energy during long working hours.",
        },
        {
            "name": "Stylish Water Bottle",
            "min_age": 10,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Sports", "Travel", "Fitness"],
            "social_tags": ["hydration", "gym-bag", "desk-setup"],
            "social_trend_score": 7.6,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1542959405-95fddf2c51df?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=insulated+water+bottle",
            "why_base": "Practical, eco‑friendly, and doubles as a subtle style accessory.",
        },
        {
            "name": "Mindfulness & Meditation App Pass",
            "min_age": 16,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Doctor", "Teacher", "Engineer", "Artist"],
            "hobby_tags": ["Self-care", "Reading"],
            "social_tags": ["mental-health", "wellness"],
            "social_trend_score": 7.8,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1525097487452-6278ff080c31?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.headspace.com/",
            "why_base": "Great for busy minds who could use pockets of calm built into their day.",
        },
        {
            "name": "Portable Laptop Stand",
            "min_age": 16,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Tech", "Work"],
            "social_tags": ["desk-setup", "productivity"],
            "social_trend_score": 7.9,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=laptop+stand",
            "why_base": "Helps with posture and keeps laptops cool during long sessions.",
        },
        {
            "name": "LED Alarm Clock with Ambient Light",
            "min_age": 14,
            "max_age": 60,
            "gender_pref": "Any",
            "profession_match": ["Student", "Teacher", "Engineer", "Artist"],
            "hobby_tags": ["Self-care"],
            "social_tags": ["room-decor", "morning-routine"],
            "social_trend_score": 7.5,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1431460481582-185fcd26b9c1?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=led+alarm+clock",
            "why_base": "Makes mornings gentler and nights more ambient with soft lighting.",
        },
        {
            "name": "Travel Journal",
            "min_age": 14,
            "max_age": 70,
            "gender_pref": "Any",
            "profession_match": ["Student", "Artist", "Teacher"],
            "hobby_tags": ["Travel", "Writing"],
            "social_tags": ["travel-vlog", "memories"],
            "social_trend_score": 7.4,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1526498460520-4c246339dccb?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=travel+journal",
            "why_base": "For the one who collects moments and stories from every trip.",
        },
        {
            "name": "Compact DSLR Camera",
            "min_age": 16,
            "max_age": 55,
            "gender_pref": "Any",
            "profession_match": ["Artist", "Student"],
            "hobby_tags": ["Photography", "Travel"],
            "social_tags": ["photo-walk", "content-creation"],
            "social_trend_score": 8.7,
            "price_range": "$$$",
            "image_url": "https://images.unsplash.com/photo-1516031190212-da133013de50?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=compact+dslr",
            "why_base": "A serious tool for creators ready to level up from phone photography.",
        },
        {
            "name": "Esports Gaming Gift Card",
            "min_age": 13,
            "max_age": 35,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer"],
            "hobby_tags": ["Gaming"],
            "social_tags": ["esports", "gaming-setup"],
            "social_trend_score": 8.5,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1593642532400-2682810df593?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://store.steampowered.com/digitalgiftcards/",
            "why_base": "Lets them choose in‑game items, passes, or new games they’re excited about.",
        },
        {
            "name": "Fashion Accessory Box",
            "min_age": 14,
            "max_age": 40,
            "gender_pref": "Any",
            "profession_match": ["Student", "Artist"],
            "hobby_tags": ["Fashion"],
            "social_tags": ["outfit-inspo", "aesthetic"],
            "social_trend_score": 7.9,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1528701800489-20be3c30c1d1?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=fashion+accessory+box",
            "why_base": "Perfect for someone who loves to experiment with outfits and styles.",
        },
        {
            "name": "Compact Action Camera",
            "min_age": 15,
            "max_age": 45,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Artist"],
            "hobby_tags": ["Travel", "Sports"],
            "social_tags": ["vlogging", "adventure"],
            "social_trend_score": 8.8,
            "price_range": "$$$",
            "image_url": "https://images.unsplash.com/photo-1526178613552-2b45c6c302f0?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=action+camera",
            "why_base": "Ideal for capturing hikes, rides, and all types of outdoor adventures.",
        },
        {
            "name": "Home Barista Kit",
            "min_age": 18,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Engineer", "Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Cooking"],
            "social_tags": ["home-cafe", "coffee"],
            "social_trend_score": 8.2,
            "price_range": "$$$",
            "image_url": "https://images.unsplash.com/photo-1459755486867-b55449bb39ff?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=barista+kit",
            "why_base": "Great for the coffee nerd who loves crafting café‑style drinks at home.",
        },
        {
            "name": "Smart Home Speaker",
            "min_age": 16,
            "max_age": 65,
            "gender_pref": "Any",
            "profession_match": ["Engineer", "Doctor", "Teacher", "Artist", "Student"],
            "hobby_tags": ["Music", "Tech"],
            "social_tags": ["smart-home", "voice-assistant"],
            "social_trend_score": 8.6,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1518445695511-067f0ebf5303?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=smart+speaker",
            "why_base": "From music and timers to smart‑home control, it becomes a daily companion.",
        },
        {
            "name": "Gym Bag Essentials Kit",
            "min_age": 16,
            "max_age": 55,
            "gender_pref": "Any",
            "profession_match": ["Engineer", "Doctor", "Teacher"],
            "hobby_tags": ["Sports", "Fitness"],
            "social_tags": ["gym", "fitness-reels"],
            "social_trend_score": 8.0,
            "price_range": "$$",
            "image_url": "https://images.unsplash.com/photo-1526401485004-2fa806b5aa66?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=gym+bag+essentials",
            "why_base": "Filled with handy add‑ons that make workouts smoother and more stylish.",
        },
        {
            "name": "Desk RGB Light Bar",
            "min_age": 13,
            "max_age": 40,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Artist"],
            "hobby_tags": ["Gaming", "Music"],
            "social_tags": ["desk-setup", "rgb"],
            "social_trend_score": 8.7,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1517059224940-d4af9eec41e5?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=monitor+light+bar+rgb",
            "why_base": "Throws moody ambient light behind their monitor or TV for extra vibes.",
        },
        {
            "name": "Tech Gadget Organizer Pouch",
            "min_age": 14,
            "max_age": 60,
            "gender_pref": "Any",
            "profession_match": ["Student", "Engineer", "Doctor", "Teacher", "Artist"],
            "hobby_tags": ["Travel", "Tech"],
            "social_tags": ["what's-in-my-bag", "minimalism"],
            "social_trend_score": 7.8,
            "price_range": "$",
            "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=800&q=80",
            "buy_link": "https://www.amazon.com/s?k=tech+organizer+pouch",
            "why_base": "Keeps chargers, cables, and gadgets neat in a bag or backpack.",
        },
    ]

    df = pd.DataFrame(gifts)
    return df


@st.cache_data(show_spinner=False)
def get_gift_df() -> pd.DataFrame:
    return build_gift_dataset()


# -----------------------------
# Matching & Scoring Logic
# -----------------------------
def compute_match_score(
    gift: pd.Series,
    age: int,
    gender: str,
    professions: List[str],
    hobbies: List[str],
    social_interests: str,
) -> float:
    score = float(gift["social_trend_score"])  # base signal

    # Age fit
    if gift["min_age"] <= age <= gift["max_age"]:
        score += 3.0
    else:
        # soft penalty if out of range
        score -= 2.0

    # Gender preference
    if gift["gender_pref"] == "Any" or gift["gender_pref"].lower() == gender.lower():
        score += 1.5

    # Profession overlap
    if professions:
        match_count = len(set(professions) & set(gift["profession_match"]))
        score += match_count * 1.8

    # Hobby overlap
    if hobbies:
        match_count = len(set(hobbies) & set(gift["hobby_tags"]))
        score += match_count * 2.2

    # Fuzzy match with social interest text
    social_interests = (social_interests or "").strip().lower()
    if social_interests:
        tags = " ".join(gift["social_tags"]).lower()
        ratio = difflib.SequenceMatcher(None, social_interests, tags).ratio()
        if ratio > 0.25:
            score += ratio * 8.0

    return score


def recommend_gifts(
    df: pd.DataFrame,
    age: int,
    gender: str,
    professions: List[str],
    hobbies: List[str],
    social_interests: str,
    top_k: int = 10,
) -> pd.DataFrame:
    # Filter by a relaxed age window first to keep scoring efficient
    rough = df[
        (df["min_age"] - 8 <= age) & (df["max_age"] + 8 >= age)
    ].copy()
    if rough.empty:
        rough = df.copy()

    scores = []
    for _, row in rough.iterrows():
        scores.append(compute_match_score(row, age, gender, professions, hobbies, social_interests))
    rough["match_score"] = scores

    rough = rough.sort_values("match_score", ascending=False)
    return rough.head(top_k)


# -----------------------------
# UI Helpers
# -----------------------------
def render_header():
    st.markdown(
        """
        <div style="margin-bottom: 0.75rem;">
            <div class="hero-badge">
                <span>🎁 Smart Gift Recommender</span>
                <span>·</span>
                <span>One form, endless ideas</span>
            </div>
            <h2 class="hero-gradient-text" style="font-size: 1.7rem; margin: 0 0 0.15rem 0;">
                Find a gift that actually feels like them.
            </h2>
            <p style="font-size: 0.95rem; color: #475569; max-width: 34rem;">
                Use the sidebar to describe who you're shopping for — we’ll score dozens of curated gifts
                by age, profession, hobbies, and even the kind of content they binge online.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendations(recs: pd.DataFrame):
    if recs.empty:
        st.warning("No strong matches yet — try broadening the age range, hobbies, or social interests.")
        return

    # Display in responsive grid
    cols_per_row = 2 if st.get_option("theme.base") == "light" else 2
    for i in range(0, len(recs), cols_per_row):
        row_slice = recs.iloc[i : i + cols_per_row]
        cols = st.columns(len(row_slice))
        for col, (_, gift) in zip(cols, row_slice.iterrows()):
            with col:
                st.markdown(
                    f"""
                    <div class="gift-card">
                        <img src="{gift['image_url']}" alt="{gift['name']}" 
                             style="width: 100%; border-radius: 12px; object-fit: cover; max-height: 180px; margin-bottom: 0.6rem;">
                        <div class="gift-title">{gift['name']}</div>
                        <div class="gift-meta">
                            <span class="gift-price">{gift['price_range']}</span>
                            <span style="margin: 0 0.25rem;">•</span>
                            <span>Trend score: {gift['social_trend_score']:.1f}</span>
                        </div>
                        <div class="gift-why">
                            {gift['why_base']}
                        </div>
                        <div style="margin-top: 0.7rem;">
                            <a class="gift-btn" href="{gift['buy_link']}" target="_blank" rel="noopener noreferrer">
                                Buy Now (placeholder)
                            </a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# -----------------------------
# Main App
# -----------------------------
def main():
    inject_global_styles()

    if "intro_shown" not in st.session_state:
        run_intro_animation()
        st.session_state["intro_shown"] = True

    df = get_gift_df()

    # Sidebar inputs
    with st.sidebar:
        st.markdown("### 🎯 Gift Receiver Profile")

        age = st.slider("Age", min_value=1, max_value=100, value=25)

        gender = st.selectbox(
            "Gender",
            options=["Male", "Female", "Other"],
            index=0,
        )

        profession_options = ["Student", "Engineer", "Teacher", "Doctor", "Artist"]
        professions = st.multiselect(
            "Profession (can pick multiple)",
            options=profession_options,
            default=["Student"],
        )

        hobby_options = ["Gaming", "Reading", "Sports", "Cooking", "Travel", "Music"]
        hobbies = st.multiselect(
            "Hobbies & interests",
            options=hobby_options,
            default=["Music", "Travel"],
        )

        social_interests = st.text_input(
            "What kind of content do they love online?",
            placeholder="e.g., fitness reels, tech gadgets, cozy booktok, fashion hauls",
        )

        st.markdown("---")
        auto_refresh = st.checkbox("Update recommendations automatically", value=True)
        search_clicked = st.button("✨ Find Gift Ideas", type="primary")

    render_header()

    should_compute = auto_refresh or search_clicked

    if should_compute:
        with st.spinner("Scoring gifts based on their vibe and lifestyle..."):
            recs = recommend_gifts(df, age, gender, professions, hobbies, social_interests)
        st.subheader("Top Gift Matches")
        render_recommendations(recs)
    else:
        st.info("Use the sidebar to fill in their details, then click **Find Gift Ideas**.")


if __name__ == "__main__":
    main()
