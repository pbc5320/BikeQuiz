
import streamlit as st
from collections import Counter
import pandas as pd

st.set_page_config(page_title="Bike Part Personality Quiz", page_icon="🚲")

st.title("🚲 Which Part of the Bicycle Are You?")
st.write("Answer the questions below. When you're done, click **Get my result** to see your bike-part match.")

st.divider()

questions = [
    {
        "q": "1) In a group project, you’re the one who…",
        "opts": {
            "A — Steers the group in the right direction.": "A",
            "B — Holds everything together when things get messy.": "B",
            "C — Keeps everyone motivated and moving forward.": "C",
            "D — Smoothly connects people and ideas.": "D",
            "E — Tracks the details no one else notices.": "E",
            "F — Adds a spark of fun and makes it enjoyable.": "F",
        },
    },
    {
        "q": "2) When faced with a big challenge, your instinct is to…",
        "opts": {
            "A — Take charge and plot the course.": "A",
            "B — Stay grounded and reliable no matter what.": "B",
            "C — Push harder until it’s done.": "C",
            "D — Shift gears and adapt to what’s needed.": "D",
            "E — Double-check everything to prevent mistakes.": "E",
            "F — Lighten the mood and keep people engaged.": "F",
        },
    },
    {
        "q": "3) Your friends would describe you as…",
        "opts": {
            "A — A leader.": "A",
            "B — Dependable.": "B",
            "C — Determined.": "C",
            "D — Flexible.": "D",
            "E — Observant.": "E",
            "F — Fun.": "F",
        },
    },
    {
        "q": "4) On a trip, your role in the group is…",
        "opts": {
            "A — The navigator with the plan.": "A",
            "B — The one carrying the load.": "B",
            "C — The timekeeper who keeps everyone moving.": "C",
            "D — The connector who introduces people and plans meetups.": "D",
            "E — The logistics brain who checks details and reservations.": "E",
            "F — The storyteller who makes it an adventure.": "F",
        },
    },
    {
        "q": "5) On a tough day, you…",
        "opts": {
            "A — Keep your eyes on the big picture.": "A",
            "B — Stay steady and supportive for others.": "B",
            "C — Push yourself (and the team) to keep going.": "C",
            "D — Adjust quickly until you find a smoother path.": "D",
            "E — Quietly fix things before they cause issues.": "E",
            "F — Remind everyone to smile and breathe.": "F",
        },
    },
    {
        "q": "6) If you were a tool, you’d be…",
        "opts": {
            "A — A compass.": "A",
            "B — A sturdy toolbox.": "B",
            "C — A power drill.": "C",
            "D — A multi-tool.": "D",
            "E — A level/ruler.": "E",
            "F — A whistle.": "F",
        },
    },
    {
        "q": "7) Your working style is closest to…",
        "opts": {
            "A — Set direction first, then execute.": "A",
            "B — Build a solid foundation and protect it.": "B",
            "C — Drive momentum and keep pace high.": "C",
            "D — Adapt on the fly and keep things linked.": "D",
            "E — Checklists, QA, and risk-proofing.": "E",
            "F — Energize the room and keep it human.": "F",
        },
    },
    {
        "q": "8) When teammates disagree, you…",
        "opts": {
            "A — Facilitate and choose a course.": "A",
            "B — Stabilize the team so emotions don’t break things.": "B",
            "C — Focus on action so you don’t stall.": "C",
            "D — Translate perspectives so people understand each other.": "D",
            "E — Surface the facts and constraints.": "E",
            "F — Diffuse tension with respectful levity.": "F",
        },
    },
]

parts = {
    "A": {
        "name": "Handlebars",
        "emoji": "🛞",
        "blurb": "Guide & orient. You steer toward clear goals and help others balance along the way."
    },
    "B": {
        "name": "Frame",
        "emoji": "🛠️",
        "blurb": "Backbone & stability. You provide structure, safety, and consistency under pressure."
    },
    "C": {
        "name": "Pedals",
        "emoji": "⚡",
        "blurb": "Drive & momentum. You supply the effort that turns plans into forward motion."
    },
    "D": {
        "name": "Chain",
        "emoji": "⛓️",
        "blurb": "Connection & adaptability. You link people and ideas, shifting smoothly between roles."
    },
    "E": {
        "name": "Brakes",
        "emoji": "🛑",
        "blurb": "Judgment & protection. You spot risks early and know when to slow down or stop."
    },
    "F": {
        "name": "Bell",
        "emoji": "🔔",
        "blurb": "Signal & spark. You keep things human—bringing attention, clarity, and joy when needed."
    },
}

# Collect answers
choices = []
for i, q in enumerate(questions):
    ans = st.radio(q["q"], list(q["opts"].keys()), index=None, key=f"q{i}")
    if ans is not None:
        choices.append(q["opts"][ans])

st.divider()
col1, col2 = st.columns([1,1])

with col1:
    if st.button("Get my result"):
        if len(choices) == 0:
            st.warning("Please answer at least one question to see your result.")
        else:
            counts = Counter(choices)
            highest = max(counts.values())
            winners = [k for k, v in counts.items() if v == highest]

            if len(winners) == 1:
                k = winners[0]
                st.success(f"**You are the {parts[k]['name']} {parts[k]['emoji']}**")
                st.write(parts[k]["blurb"])
            else:
                # Handle ties: show blended identity
                names = ", ".join([parts[k]["name"] for k in winners])
                st.info(f"**You are a blend:** {names}")
                for k in winners:
                    st.write(f"- **{parts[k]['name']} {parts[k]['emoji']}** — {parts[k]['blurb']}")

            st.subheader("Your answer breakdown")
            # Build a DataFrame for charting
            df = pd.DataFrame({
                "Part": [parts[k]["name"] for k in parts.keys()],
                "Count": [counts.get(k, 0) for k in parts.keys()],
            })
            st.bar_chart(df, x="Part", y="Count", use_container_width=True)

with col2:
    # Educator controls & export
    st.caption("Educator tools")
    if choices:
        from io import StringIO
        counts = Counter(choices)
        highest = max(counts.values())
        winners = [k for k, v in counts.items() if v == highest]
        winner_names = ", ".join(parts[k]["name"] for k in winners)
        buf = StringIO()
        buf.write("Bike Part Personality Quiz Result\n")
        buf.write("-------------------------------\n")
        buf.write(f"Top match: {winner_names}\n")
        for k in parts:
            buf.write(f"{parts[k]['name']}: {counts.get(k, 0)}\n")
        st.download_button("Download my result (.txt)", data=buf.getvalue(), file_name="bike_quiz_result.txt")

st.divider()
with st.expander("Teacher setup notes"):
    st.markdown("""
- **Run locally:**  
  1. Install with `pip install streamlit`.  
  2. Save this file as `bike_quiz_streamlit.py`.  
  3. Run: `streamlit run bike_quiz_streamlit.py`  
- **Share online (free):** Push this file to a public GitHub repo and deploy on [Streamlit Community Cloud](https://streamlit.io/cloud).
- **Privacy tip:** No personal data is stored by default. If you need class analytics, add a name/ID input and write results to a CSV.
""")

