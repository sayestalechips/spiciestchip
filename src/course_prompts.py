"""
Module containing all course-specific prompts and tools for ChipGPT
"""

from typing import Dict, Optional

# Icebreaker Tools Dictionary
ICEBREAKER_TOOLS = {
    "1-Word Story": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190167",
        "description": "A collaborative storytelling exercise for groups of up to 10 participants. Participants create a cohesive story by adding one word at a time, aiming to end on a pre-selected target word. Ideal for fostering creativity and teamwork in 4-7 minutes."
    },
    "2 Truths and a Lie": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190168",
        "description": "An engaging icebreaker for groups of 5-7 participants. Each person shares two true statements and one lie about themselves, encouraging connection and learning among team members. Takes 10-20 minutes and is perfect for starting a session or break."
    },
    "5 Second Test": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190169",
        "description": "A quick drawing exercise for unlimited participants. In just 5 seconds, participants must sketch a given topic, building confidence in visual communication. Ideal for kickstarting creativity before brainstorming sessions, taking 3-7 minutes."
    },
    "Animal Noises": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190170",
        "description": "A hilarious, high-energy icebreaker for any group size. Participants act and sound like animals for 20 seconds, creating a playful atmosphere. Perfect for adjusting the room's energy or clearing minds in just 1-3 minutes."
    },
    "Best Day Ever!": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190171",
        "description": "A quick reflection exercise for groups of 4-10. Participants describe their greatest day (past or imagined) in 30 seconds, fostering connections through shared experiences. Takes about 5 minutes and can be used anytime during a session."
    },
    "Bob Ross": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190173",
        "description": "An improv-based activity for groups of 4-10. Participants create a \"live painting\" by acting as elements in a scene, encouraging creativity and teamwork. Takes 7-10 minutes and is great for re-energizing after breaks or mentally strenuous activities."
    },
    "Cake": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190174",
        "description": "A lateral thinking puzzle for unlimited participants. Players must find creative ways to cut a cake into 8 equal pieces with just 3 cuts, encouraging out-of-the-box thinking. Takes 5-7 minutes and is ideal for transitioning to creative thinking exercises."
    },
    "Cape of Compliments": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190175",
        "description": "A positive, affirming activity for any group size. Participants write compliments on each other's \"capes,\" fostering a supportive environment. Takes 10-20 minutes and is perfect for wrapping up a session or following a stressful moment."
    },
    "Clue": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190176",
        "description": "An interactive detective game for up to 10 participants. Players become both detectives and suspects, uncovering fun facts about each other. Takes 10-15 minutes and is great for starting a session or break."
    },
    "Comic Book": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190177",
        "description": "A deep connection exercise for groups of 4-6. Participants create a comic book of their life, sharing pivotal moments through drawings and brief text. Takes 20-30 minutes and is ideal for beginning a session or after a break."
    },
    "Dance Moves": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190179",
        "description": "A quick, high-energy icebreaker led by the facilitator. By performing an intentionally awkward dance move, the facilitator sets a tone of vulnerability and creativity. Takes 2-4 minutes and is perfect for starting a session or energizing after a break."
    },
    "Dice": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190180",
        "description": "A simple, fun introduction game for groups of 5-10. Using a die with prompts, participants share lesser-known facts about themselves, building trust and connection. Takes 5-8 minutes and works well before diving into more serious content."
    },
    "Draw Yourself": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190182",
        "description": "A creative introduction exercise for up to 30 participants. Instead of verbal introductions, participants draw themselves and aspects of their lives, providing a unique snapshot of each person. Takes 8-12 minutes and is great for starting complex exercises or after a break."
    },
    "Favorite Picture": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/40817666",
        "description": "A personal sharing activity for groups of 5-7. Participants find and share their favorite picture with a meaningful story behind it, fostering trust and connection. Takes just 2 minutes and is suitable for starting a session or after a break."
    },
    "Favorite Song": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/40817636",
        "description": "An energetic, music-based activity for 6-20 participants. Players walk around the room playing their favorite songs, creating a fun atmosphere of controlled chaos. Takes 5-7 minutes and is great for transitions or after breaks."
    },
    "Giraffe Gaffe": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190183",
        "description": "A silly, energizing activity for any group size. Participants attempt to create an origami giraffe behind their backs in just one minute, encouraging laughter and engagement. Takes 8-12 minutes and works well before complex exercises or after breaks."
    },
    "Globetrotter": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190184",
        "description": "An interactive geography game for groups of 5-7. Using an inflatable globe, participants share facts about different locations, building trust and easing collaboration. Takes 4-6 minutes and is ideal for starting a session or break."
    },
    "Greatest Connection": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190248",
        "description": "A networking activity for unlimited participants. Players seek to find the most interesting connection between two people in the room, encouraging active listening and relationship building. Takes about 7 minutes for 50 participants and is great for starting sessions or breaks."
    },
    "Human Machine": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/40817671",
        "description": "A physical version of \"Telephone\" for 5-25 participants. Players create a chain of movements, watching how the original action morphs through the group. Takes 5-7 minutes and is perfect for changing the room's atmosphere or transitioning between exercises."
    },
    "Improv Stick": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190249",
        "description": "An improv exercise for groups of 10-25. Using a simple prop, participants demonstrate various objects or actions, encouraging creativity and quick thinking. Takes 7 minutes and is great for starting a session or energizing after a break."
    },
    "Nike Check": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190251",
        "description": "A creative thinking exercise for any group size. Participants draw Nike \"swooshes\" and transform them into other objects, promoting lateral thinking. Takes 5-7 minutes and is ideal for warming up before brainstorming or starting a session."
    },
    "Ninja Tiger Grandma": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190253",
        "description": "An energetic, sound-based version of Rock Paper Scissors for even-numbered groups. Participants act out Ninja, Tiger, or Grandma in a fun, competitive game. Takes 3-5 minutes and is perfect for boosting energy levels at any point in a session."
    },
    "NYT 36": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190255",
        "description": "A powerful connection exercise inspired by the New York Times' \"36 questions to fall in love.\" Participants rotate and answer thought-provoking questions, fostering deep connections. Takes 5-8 minutes and works well at the start of a session or after breaks."
    },
    "One-handed Airplane": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190256",
        "description": "A collaborative paper airplane challenge for pairs. Teams must create a paper airplane using only one hand each, promoting communication and teamwork. Takes 5-8 minutes and is great for starting a session or energizing the group."
    },
    "Phone Call": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190271",
        "description": "A role-playing exercise for 20+ participants. Players simulate a phone call with their best friend, revealing habits, emotions, and building group camaraderie. Takes 5-10 minutes and is ideal for starting a session or boosting energy."
    },
    "Questions": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190274",
        "description": "A simple yet effective discussion starter for groups of 3-7. Using thought-provoking questions, this exercise generates interesting conversations and builds trust. Takes 7-15 minutes and works well before or after serious content."
    },
    "Remember When": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190276",
        "description": "An improv-based storytelling exercise for groups of 5-7. Participants collaboratively create a story using \"Remember when...\" prompts, fostering creativity and teamwork. Takes 8-15 minutes and is great for starting a session or after a break."
    },
    "Roman Numeral": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190277",
        "description": "A lateral thinking puzzle for unlimited participants. Players must transform the Roman numeral IX into VI using one continuous line, encouraging creative problem-solving. Takes 5-9 minutes and is perfect before brainstorming or after breaks."
    },
    "Roving Reporter": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/40817653",
        "description": "A interview-style activity for groups of 5-12. Participants ask and answer meaningful questions, creating connections and shared stories. Takes 15-20 minutes and is ideal for diving into a session or after a break."
    },
    "RPS": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190278",
        "description": "An energetic, team-building version of Rock Paper Scissors for 5-5,000 participants. Losers become cheerleaders for winners, creating a fun, supportive atmosphere. Takes about 4 minutes and is great before serious exercises or after breaks."
    },
    "Silent Time": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190280",
        "description": "A calming, reflective exercise for any group size. Participants silently contemplate a given topic, providing a mental break in chaotic workshops. Takes 3-7 minutes and is perfect for lowering energy levels or after intense modules."
    },
    "Similarities": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190319",
        "description": "A team-building exercise for groups of 4-7. Participants find shared similarities and create a fictional story of how they met, fostering connections and creativity. Takes 10-16 minutes and works well before serious exercises or after breaks."
    },
    "Star Wars": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190320",
        "description": "A high-energy, imaginative exercise for 15+ participants. The group engages in a mock lightsaber battle, encouraging playfulness and creativity. Takes 2-4 minutes and is great for transitioning between serious topics or after breaks."
    },
    "Super Powers": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190321",
        "description": "A fun introduction exercise for 10-20 participants. Each person shares their name, a proud skill, and a desired superpower, creating connections through storytelling. Takes 8-15 minutes and is ideal for starting a session or after breaks."
    },
    "Virtual Song": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190337",
        "description": "An energizing virtual activity for 6-20 participants. Players silently jam to their favorite songs on camera, creating a fun, shared experience. Takes 5-7 minutes and is perfect for starting a virtual session or boosting energy."
    },
    "Worst Quality": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/39190339",
        "description": "A vulnerability-building exercise for groups of 5-7. Participants share their perceived worst quality, fostering connection through openness. Takes 5-8 minutes and works well for starting a session or re-energizing after lunch."
    },
    "Yes And": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/40817661",
        "description": "An improv-based exercise for pairs. Participants practice building on each other's ideas using \"Yes, and...\" responses, encouraging positive collaboration. Takes 6-10 minutes and is great before design thinking processes or to start a session."
    },
    "No Work, No Family": {
        "url": "https://stalechips.teachable.com/courses/1732552/lectures/41173472",
        "description": "A deep-dive introduction exercise for groups of 5-12. Participants share about themselves without mentioning work or family, encouraging more profound connections. Takes 6-10 minutes and is ideal before serious exercises or after breaks."
    }
}

# Brainstorming Tools Dictionary
BRAINSTORMING_TOOLS = {
    "Brainwriting": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185862",
        "description": "A tactic for rapidly generating lots and lots of ideas by creating a time-crunch and encouraging \"yes-and\" thinking. Participants create an initial idea before chaos creates diamonds. Using the concepts of others and the pressure of time, participants will generate 8 fresh concepts in less than 8 minutes.",
        "complexity": "Medium",
        "participants": "5-7 participants per group, can have multiple groups",
        "time": "10-15 mins",
        "materials": "Sheet of paper folded into equal rectangles, sharpies for each participant"
    },
    "Medici Method": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185894",
        "description": "This famous family of old Florence, Italy were known for their wealth... and their sticky fingers. While we don't condone stealing, we do love being inspired by the ideas of others. We don't always need to reinvent the wheel to reinvent the art of our possible.",
        "complexity": "Easy",
        "participants": "4-7 participants per group, can have multiple groups",
        "time": "10-25 mins",
        "materials": "Flip charts, sharpies for each person, wall space, pre-defined inspiration"
    },
    "Index Funned": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185888",
        "description": "A toolkit that anonymizes how we build and support one another's ideas. Using prompts to gather individual, isolated responses, the group benefits from a blending of minds to arrive at improved thoughts and discussions. Remember: time up means time up!",
        "complexity": "Easy",
        "participants": "Unlimited number of participants, no more than 2 cards/prompts per Index Funned",
        "time": "8-15 minutes",
        "materials": "Index cards, pens, optional to print out with space for voting on back"
    },
    "Card Pass": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185888",
        "description": "Similar to Index Funned, this exercise anonymizes idea sharing and building. Participants pass cards around, adding to or rating ideas, creating a collaborative brainstorming process.",
        "complexity": "Easy",
        "participants": "Unlimited number of participants, no more than 2 cards/prompts per Card Pass",
        "time": "8-15 minutes",
        "materials": "Index cards, pens"
    },
    "Forced Connections": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185882",
        "description": "The human brain loves predictability and patterns. To help short-circuit traditional ideas, this tool forces participants to make connections from seemingly unrelated concepts, serving as a framework for the freedom of ideation and getting the group outside of the box.",
        "complexity": "Medium",
        "participants": "4-7 participants per group, can have multiple groups",
        "time": "15-25 minutes",
        "materials": "Post-its & Sharpies for each participant, prepped inspiration cards"
    },
    "100 Pics": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185840",
        "description": "A brainstorming technique that uses random pictures to inspire ideas. Like the big bang, this is all about intentionally creating chaos to spark an explosion of ideas, generating many concepts in search of a handful of great ones.",
        "complexity": "Medium",
        "participants": "4-7 participants per group, can have multiple groups",
        "time": "10-15 minutes",
        "materials": "Random pictures, writing materials"
    },
    "Art Show": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185841",
        "description": "An exercise where participants create visual representations of their ideas and share them gallery-style. Silently, they rotate around the room observing, stealing, and combining ideas from others into new opportunities.",
        "complexity": "Medium",
        "participants": "As many as desired",
        "time": "10-15 minutes",
        "materials": "Large paper or boards, drawing materials"
    },
    "Batter's Box": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185843",
        "description": "A tactic for organizing group presentations and discussions. Using a central area for presentations and a second area prepped for sharing, this exercise encourages effective communication and preparation of thoughts.",
        "complexity": "Easy",
        "participants": "Unlimited. More of a tactic used for organizing the group",
        "time": "6-8 minutes",
        "materials": "Designated presentation space, preparation area"
    },
    "Brain Vomit": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185843",
        "description": "A technique that helps shake off nervousness around creativity and gets the ball rolling toward filter-free ideation. It cuts off the feedback loop and emphasizes quantity of ideas over quality.",
        "complexity": "Easy",
        "participants": "4-12 participants (can be divided into smaller groups)",
        "time": "7-12 minutes",
        "materials": "Paper and writing materials for all participants"
    },
    "Bucket Bonanza": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185865",
        "description": "A method for gathering anonymous ideas from the crowd using a bucket. Participants write ideas on paper and drop them in the bucket, allowing for hidden ideas to be read aloud or reviewed for future use.",
        "complexity": "Easy",
        "participants": "5-7 participants in a group seated at a table",
        "time": "8-10 minutes",
        "materials": "Paper slips, writing materials, bucket or container"
    },
    "Creativity Matrix": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185869",
        "description": "A structured exercise designed to foster innovative ideas by forcing connections between different categories and user groups. This method encourages participants to generate ideas within a defined framework, ensuring clarity and focus.",
        "complexity": "Medium",
        "participants": "Up to 5 participants per group, can have multiple groups",
        "time": "20-25 minutes",
        "materials": "Large board or flip charts, Post-it notes, Sharpies"
    },
    "Crazy Eights": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185867",
        "description": "Timeboxed, intense ideation. It can feel overwhelming, but this pressure cooker of a brainstorming exercise forces participants to create concepts 'filter-free' because there is no time to question the quality of a concept.",
        "complexity": "Medium",
        "participants": "Individually completed, 3-10 participants in group sharing",
        "time": "10-12 minutes",
        "materials": "Paper and writing materials for each participant"
    },
    "Objective-ly Good": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185896",
        "description": "Similar to 'Forced Connections', this tool inspires participants to create new concepts based on physical objects. See-Think-Create! Rapid and simple to organize, 'Objectively Good' bounces between hilariously bad and incredibly great ideas.",
        "complexity": "Medium",
        "participants": "5-7 participants per group, can have multiple groups",
        "time": "10-15 minutes",
        "materials": "Physical objects for inspiration, writing materials"
    },
    "Parking Lot": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185905",
        "description": "A tool to maintain focus on the objective by redirecting off-topic conversations. It allows for kindly adjusting the conversation flow by 'parking' ideas for further discussion later.",
        "complexity": "Easy",
        "participants": "Unlimited Participants",
        "time": "1-3 minutes",
        "materials": "Designated space for 'parking' ideas, writing materials"
    },
    "Product Box": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185906",
        "description": "Instead of building 'the thing', create an effective description. This tool is used to summarize a concept, create a clearer storyline around the project or product, and allow for rapid sharing outside of the workshop.",
        "complexity": "Medium",
        "participants": "5-8 participants per group, can have multiple groups",
        "time": "25-45 minutes",
        "materials": "Materials for creating product packaging/presentation"
    },
    "SCAMPER": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185907",
        "description": "An acronym for a tool used by product teams and creative parties to generate a massive quantity of ideas from a single concept. By forcing the mind to ideate through specific 'filters', the group can generate a significant number of concepts in a condensed amount of time.",
        "complexity": "Medium",
        "participants": "5-7 participants per group, can have multiple groups",
        "time": "15-25 minutes",
        "materials": "SCAMPER worksheet, writing materials"
    },
    "Worst Idea": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185919",
        "description": "When the groups get stuck on perfection, hit the reset button. This tactical brainstorming tool forces the team to look away from the ideal and make a horrifically bad, comical concept. By separating ideation from efficiency, greater inspiration can be tapped into.",
        "complexity": "Easy",
        "participants": "5-7 participants per group, as many groups as needed",
        "time": "10-20 minutes",
        "materials": "Writing materials, sense of humor"
    },
    "If I were": {
        "url": "https://stalechips.teachable.com/courses/1732284/lectures/39185895",
        "description": "A brainstorming tool that thrives on inspiration and imagination. Don't walk a mile in another's shoes; instead, ideate 1,000 new concepts from their point of view. How would Walt Disney solve this same problem?",
        "complexity": "Medium",
        "participants": "5-7 participants per group is ideal",
        "time": "10-15 minutes",
        "materials": "Writing materials, reference materials for chosen perspectives"
    }
}

# Utility functions
def get_tool_info(tool_name: str, tool_type: str = "icebreaker") -> Optional[Dict]:
    """Get information about a specific tool."""
    if tool_type == "icebreaker":
        return ICEBREAKER_TOOLS.get(tool_name)
    elif tool_type == "brainstorming":
        return BRAINSTORMING_TOOLS.get(tool_name)
    return None

def get_all_tools(tool_type: str = "icebreaker") -> Dict:
    """Get all tools of a specific type."""
    if tool_type == "icebreaker":
        return ICEBREAKER_TOOLS
    elif tool_type == "brainstorming":
        return BRAINSTORMING_TOOLS
    return {}

# Course prompts dictionary
COURSE_PROMPTS = {
    'icebreakers': ICEBREAKER_TOOLS,  # The full prompt you provided earlier
    'brainstorming': None,  # We'll add this next
    # Other course prompts will be added here
}

PERSONALITIES = {
    "Bossy Boss": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188790",
        "description": "A facilitation technique for managing dominant personalities in group settings. Useful for workshops or meetings with 5-15 participants, especially when dealing with authoritative figures who tend to control discussions.",
        "characteristics": [
            "Tends to dominate conversations",
            "Makes unilateral decisions",
            "May interrupt others",
            "Strong opinions and presence"
        ],
        "management_tips": [
            "Establish clear ground rules at the start",
            "Use structured turn-taking exercises",
            "Acknowledge their experience while creating space for others",
            "Channel their energy into productive leadership roles"
        ],
        "recommended_tools": ["Parking Lot", "Batter's Box", "Art Show"]
    },
    "Shy Sam": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188794",
        "description": "A facilitation technique for encouraging participation from reserved individuals in group settings. Ideal for meetings or workshops with 5-20 participants, particularly useful when trying to draw out ideas from quieter team members.",
        "characteristics": [
            "Hesitant to speak up",
            "May have valuable insights but rarely shares",
            "Prefers written communication",
            "Often overshadowed by louder voices"
        ],
        "management_tips": [
            "Use written brainstorming techniques",
            "Create smaller breakout groups",
            "Provide advance notice of discussion topics",
            "Use round-robin techniques to ensure equal participation"
        ],
        "recommended_tools": ["Index Funned", "Brain Vomit", "Bucket Bonanza"]
    },
    "Seasoned Susan": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188791",
        "description": "A strategy for managing experienced team members who may be resistant to new ideas. Effective for brainstorming sessions or change management meetings with 5-15 participants, especially when dealing with long-term employees.",
        "characteristics": [
            "Extensive experience in their role",
            "May be resistant to change",
            "Often references past experiences",
            "Can be skeptical of new approaches"
        ],
        "management_tips": [
            "Acknowledge their experience and expertise",
            "Frame new ideas in context of past successes",
            "Use their knowledge as a foundation for innovation",
            "Create opportunities for them to mentor others"
        ],
        "recommended_tools": ["Medici Method", "SCAMPER", "If I were"]
    },
    "Too Cool, Must Rule": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188790",
        "description": "A technique for managing influential personalities who tend to dominate group discussions. Suitable for workshops or meetings with 5-15 participants, particularly useful when dealing with charismatic individuals who may overshadow others' contributions.",
        "characteristics": [
            "Natural leader personality",
            "Highly charismatic",
            "Can overshadow others",
            "Tends to influence group opinion"
        ],
        "management_tips": [
            "Channel their energy into constructive leadership roles",
            "Create structured sharing opportunities",
            "Use anonymous ideation techniques",
            "Balance their influence with other voices"
        ],
        "recommended_tools": ["Brain Vomit", "Index Funned", "Art Show"]
    },
    "Engineer Brain": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188796",
        "description": "An approach for engaging logical, process-oriented thinkers in creative sessions. Effective for innovation workshops or problem-solving meetings with 5-20 participants, especially when working with technical team members.",
        "characteristics": [
            "Highly analytical",
            "Process-oriented",
            "Prefers concrete data",
            "May struggle with abstract concepts"
        ],
        "management_tips": [
            "Provide clear structure and objectives",
            "Use data-driven approaches",
            "Break complex problems into smaller components",
            "Allow time for detailed analysis"
        ],
        "recommended_tools": ["Creativity Matrix", "SCAMPER", "Product Box"]
    },
    "Me First!": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188797",
        "description": "A strategy for managing self-centered behavior in group decision-making processes. Useful for prioritization sessions or collaborative planning meetings with 5-15 participants, particularly when dealing with individuals who prioritize personal interests over team goals.",
        "characteristics": [
            "Focuses on personal gain",
            "May disregard team objectives",
            "Competitive mindset",
            "Strong self-advocacy"
        ],
        "management_tips": [
            "Align personal interests with team goals",
            "Create structured sharing opportunities",
            "Emphasize collective success",
            "Use anonymous voting techniques"
        ],
        "recommended_tools": ["Index Funned", "Bucket Bonanza", "Parking Lot"]
    },
    "Negative Numpty": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188799",
        "description": "A technique for addressing persistent negativity in group settings. Effective for brainstorming or problem-solving sessions with 5-20 participants, especially when dealing with team members who tend to shoot down ideas.",
        "characteristics": [
            "Frequently criticizes ideas",
            "Focuses on problems over solutions",
            "May discourage others' participation",
            "Skeptical of new approaches"
        ],
        "management_tips": [
            "Channel criticism into constructive feedback",
            "Use 'Yes, And' techniques",
            "Establish positive ground rules",
            "Acknowledge concerns while maintaining momentum"
        ],
        "recommended_tools": ["Worst Idea", "Brain Vomit", "SCAMPER"]
    },
    "Mine. Mine. Mine": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188825",
        "description": "An approach for managing territorial behavior in collaborative environments. Suitable for cross-functional meetings or project planning sessions with 5-15 participants, particularly when dealing with individuals who are overly possessive of ideas or resources.",
        "characteristics": [
            "Protective of resources/ideas",
            "Reluctant to share control",
            "Strong ownership mentality",
            "May resist collaboration"
        ],
        "management_tips": [
            "Emphasize shared success",
            "Create collaborative exercises",
            "Acknowledge contributions explicitly",
            "Use team-based rewards"
        ],
        "recommended_tools": ["Art Show", "Medici Method", "Product Box"]
    },
    "All or Nothing": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188827",
        "description": "A strategy for managing unrealistic expectations in group decision-making. Effective for prioritization workshops or strategic planning sessions with 5-20 participants, especially when dealing with individuals who struggle to focus on key priorities.",
        "characteristics": [
            "Seeks perfection",
            "Difficulty compromising",
            "May block progress",
            "Struggles with prioritization"
        ],
        "management_tips": [
            "Break large goals into smaller steps",
            "Use structured prioritization tools",
            "Focus on progress over perfection",
            "Create clear success criteria"
        ],
        "recommended_tools": ["Creativity Matrix", "SCAMPER", "Parking Lot"]
    },
    "En Garde": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188829",
        "description": "A technique for encouraging open communication in hierarchical team structures. Useful for innovation workshops or feedback sessions with 5-15 participants, particularly when dealing with team members who are hesitant to share ideas in front of authority figures.",
        "characteristics": [
            "Defensive posture",
            "Guarded communication",
            "Sensitivity to criticism",
            "Risk-averse behavior"
        ],
        "management_tips": [
            "Create psychological safety",
            "Use anonymous sharing techniques",
            "Establish clear ground rules",
            "Provide private feedback channels"
        ],
        "recommended_tools": ["Index Funned", "Bucket Bonanza", "Brain Vomit"]
    },
    "Give me your Tired": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188830",
        "description": "An approach for re-energizing fatigued participants in extended group sessions. Effective for long workshops or multi-day planning sessions with 5-20 participants, especially when dealing with mental or physical exhaustion.",
        "characteristics": [
            "Low energy levels",
            "Decreased participation",
            "Reduced attention span",
            "May show signs of burnout"
        ],
        "management_tips": [
            "Incorporate energizing activities",
            "Schedule regular breaks",
            "Vary the pace and type of activities",
            "Be attentive to group energy levels"
        ],
        "recommended_tools": ["Brain Vomit", "Art Show", "Crazy Eights"]
    },
    "Co-Facilitator": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188854",
        "description": "A strategy for managing participants who try to take over facilitation roles. Suitable for workshops or collaborative sessions with 5-15 participants, particularly useful when dealing with experienced team members who may challenge the facilitator's authority.",
        "characteristics": [
            "Takes control of discussions",
            "Offers unsolicited facilitation",
            "May undermine planned activities",
            "Often has facilitation experience"
        ],
        "management_tips": [
            "Acknowledge their expertise",
            "Assign specific roles or responsibilities",
            "Set clear expectations upfront",
            "Channel their energy constructively"
        ],
        "recommended_tools": ["Batter's Box", "Parking Lot", "Product Box"]
    },
    "My-Job": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188856",
        "description": "An approach for addressing job security concerns in process improvement initiatives. Effective for change management workshops or efficiency planning sessions with 5-20 participants, especially when proposed changes may impact existing roles.",
        "characteristics": [
            "Defensive about role",
            "Resistant to change",
            "Concerned about job security",
            "May withhold information"
        ],
        "management_tips": [
            "Address concerns openly",
            "Focus on growth opportunities",
            "Emphasize skill development",
            "Create safe spaces for honest dialogue"
        ],
        "recommended_tools": ["Index Funned", "Bucket Bonanza", "Parking Lot"]
    },
    "Oversharer": {
        "url": "https://stalechips.teachable.com/courses/1732452/lectures/39188793",
        "description": "A technique for managing participants who dominate discussions with excessive details. Useful for brainstorming sessions or team meetings with 5-15 participants, particularly when time management is crucial for achieving meeting objectives.",
        "characteristics": [
            "Provides too much detail",
            "Often goes off-topic",
            "May consume excessive time",
            "Enthusiastic about sharing"
        ],
        "management_tips": [
            "Set clear time limits",
            "Use structured sharing formats",
            "Acknowledge contributions while staying on track",
            "Provide alternative channels for detailed input"
        ],
        "recommended_tools": ["Parking Lot", "Brain Vomit", "Bucket Bonanza"]
    }
}

AF_RANKS = {
    "ENLISTED": {
        "E1_E2": {
            "attitudes": [
                "Eager",
                "Inexperienced",
                "Overwhelmed"
            ],
            "working_style": [
                "Follows orders closely",
                "Relies heavily on supervision",
                "Focuses on mastering basic tasks"
            ],
            "education": "High school diploma"
        },
        "E3_E4": {
            "attitudes": [
                "Motivated",
                "Beginning to gain confidence",
                "Looking to prove oneself",
                "Beginning to think about career advancement"
            ],
            "working_style": [
                "Works diligently under supervision",
                "Starting to take on more responsibilities",
                "Follows procedures carefully",
                "Handles routine tasks with some independence"
            ],
            "education": "May have some college credits"
        },
        "E5": {
            "attitudes": [
                "Responsible",
                "Leadership-oriented",
                "Focused on career development"
            ],
            "working_style": [
                "Manages small teams",
                "Provides training and supervision",
                "Balances technical work with administrative duties"
            ],
            "education": "Probably has some college level courses complete"
        },
        "E6": {
            "attitudes": [
                "Experienced",
                "Reliable",
                "Professional",
                "Mentorship-focused"
            ],
            "working_style": [
                "Leads larger teams",
                "Oversees complex tasks",
                "Serves as technical expert",
                "Mentors junior NCOs and airmen"
            ],
            "education": "May have an undergraduate degree"
        },
        "E7": {
            "attitudes": [
                "Highly experienced",
                "Authoritative",
                "Respected",
                "Strategic mindset"
            ],
            "working_style": [
                "Manages multiple teams or large section",
                "Strategic thinker",
                "Balances leadership with technical expertise",
                "Often involved in policy implementation"
            ],
            "education": "Probably some or all of undergraduate degree complete"
        },
        "E8": {
            "attitudes": [
                "Senior leader",
                "Influential",
                "Strategic focus"
            ],
            "working_style": [
                "Oversees large units or organizations",
                "Involved in high-level decision-making",
                "Mentors senior NCOs",
                "Focuses on long-term goals"
            ],
            "education": "Probably undergraduate degree complete, may have graduate credits"
        },
        "E9": {
            "attitudes": [
                "Most senior enlisted rank",
                "Highly respected",
                "Influential",
                "Strategic visionary"
            ],
            "working_style": [
                "Provides strategic leadership",
                "Advises commanders",
                "Focuses on force management",
                "Implements policy at highest levels"
            ],
            "education": "Probably undergraduate complete, likely some graduate credits"
        }
    },
    "OFFICER": {
        "O1": {
            "categories": {
                "prior_enlisted": {
                    "attitudes": [
                        "Generally eager",
                        "Highly engaged",
                        "Transitioning from technical to leadership role",
                        "More experienced than peers"
                    ]
                },
                "non_prior": {
                    "attitudes": [
                        "Eager",
                        "Ambitious",
                        "Still learning the role"
                    ]
                }
            },
            "working_style": [
                "Learning to lead",
                "Taking on initial leadership responsibilities",
                "Developing leadership style"
            ],
            "education": "Undergraduate degree required"
        },
        "O2": {
            "categories": {
                "prior_enlisted": {
                    "attitudes": [
                        "Increasingly comfortable as leader",
                        "More experience than some higher ranks",
                        "Balanced technical/leadership approach"
                    ]
                },
                "non_prior": {
                    "attitudes": [
                        "More confident",
                        "Looking to refine leadership skills",
                        "Building experience base"
                    ]
                }
            },
            "working_style": [
                "Leads more effectively",
                "Takes on more complex tasks",
                "Developing personal leadership style"
            ],
            "education": "Undergraduate degree and some graduate credits"
        },
        "O3": {
            "categories": {
                "prior_enlisted": {
                    "attitudes": [
                        "Experienced",
                        "Strategic thinker",
                        "Authoritative"
                    ]
                },
                "non_prior": {
                    "attitudes": [
                        "Competent",
                        "Assertive",
                        "Responsible"
                    ]
                }
            },
            "working_style": [
                "Leads larger teams or units",
                "Manages significant projects",
                "Balances leadership with administrative duties"
            ],
            "education": "Undergraduate degree and some graduate credits"
        },
        "O4": {
            "attitudes": [
                "Experienced",
                "Learning strategic thinking",
                "Increasing authority"
            ],
            "working_style": [
                "Involved in high-level planning",
                "Manages large units or operations",
                "Mentors junior officers"
            ],
            "education": "Undergraduate degree and some graduate credits"
        },
        "O5": {
            "attitudes": [
                "Significantly more autonomy",
                "Broader responsibility span",
                "Strategic focus"
            ],
            "working_style": [
                "Commands large units",
                "Develops and implements policies",
                "Strategic planning",
                "Mentors mid-level officers"
            ],
            "education": "Undergraduate degree and likely complete graduate degree"
        },
        "O6_plus": {
            "attitudes": [
                "Highly respected",
                "Influential",
                "Strategic thinking",
                "Very confident"
            ],
            "working_style": [
                "Oversees major commands",
                "High-level strategic planning",
                "Advises senior leaders",
                "Mentors senior officers"
            ],
            "education": "Multiple advanced degrees typical"
        }
    }
}

AF_SUBCULTURES = {
    "OPERATIONAL": {
        "examples": ["Pilots", "aircrew", "special operations"],
        "focus": "Mission execution, combat readiness",
        "characteristics": [
            "High intensity",
            "Strong emphasis on teamwork",
            "Disciplined",
            "Values competitiveness over procedures"
        ],
        "communication_style": [
            "Direct",
            "Results-oriented",
            "Assertive"
        ],
        "values_info_type": [
            "Competitive analysis",
            "Performance metrics"
        ]
    },
    "MAINTENANCE": {
        "examples": ["Technicians", "avionics specialists"],
        "focus": "Aircraft and equipment maintenance",
        "characteristics": [
            "Expects hierarchy",
            "Detail-oriented",
            "Technical mindset",
            "Procedural approach"
        ],
        "communication_style": [
            "Clear",
            "Formalized",
            "Technical"
        ],
        "values_info_type": [
            "Efficiency reports",
            "Compliance data",
            "Performance metrics"
        ]
    },
    "SUPPORT_ADMIN": {
        "examples": ["Logistics", "supply chain", "personnel"],
        "focus": "Essential support services",
        "characteristics": [
            "Customer service-oriented",
            "Detail-oriented",
            "Policy-focused"
        ],
        "communication_style": [
            "Clear",
            "Formalized",
            "Service-oriented"
        ],
        "values_info_type": [
            "Efficiency reports",
            "Compliance data",
            "Customer satisfaction metrics"
        ]
    },
    "MEDICAL": {
        "examples": ["Physicians", "nurses", "medical technicians"],
        "focus": "Health and wellness",
        "characteristics": [
            "Compassionate",
            "Patient-focused",
            "Highly trained",
            "Customer service-oriented"
        ],
        "communication_style": [
            "Clear",
            "Empathetic",
            "Professional",
            "Detail-oriented"
        ],
        "values_info_type": [
            "Patient outcomes",
            "Healthcare metrics",
            "Compliance data",
            "Quality measures"
        ]
    },
    "INTELLIGENCE": {
        "examples": ["Analysts", "cyber operators"],
        "focus": "Intelligence gathering and analysis",
        "characteristics": [
            "Analytical mindset",
            "Strategic thinking",
            "Security-focused",
            "Detail-oriented"
        ],
        "communication_style": [
            "Precise",
            "Data-driven",
            "Security-conscious",
            "Methodical"
        ],
        "values_info_type": [
            "Intelligence reports",
            "Trend analysis",
            "Threat assessments",
            "Pattern recognition"
        ]
    },
    "CYBER_COMMUNICATIONS": {
        "examples": ["Cybersecurity specialists", "network admins"],
        "focus": "Secure and reliable communications",
        "characteristics": [
            "Technologically adept",
            "Problem-solving oriented",
            "Security-minded",
            "Innovation-focused"
        ],
        "communication_style": [
            "Technical",
            "Direct",
            "Solution-oriented",
            "Process-focused"
        ],
        "values_info_type": [
            "Network metrics",
            "Security reports",
            "System performance data",
            "Incident reports"
        ]
    },
    "EDUCATION_TRAINING": {
        "examples": ["Instructors", "education officers", "training specialists"],
        "focus": "Professional development and knowledge transfer",
        "characteristics": [
            "Instructional mindset",
            "Emphasis on mentorship",
            "Knowledge-sharing focused",
            "Doctrine-oriented"
        ],
        "communication_style": [
            "Educational",
            "Structured",
            "Patient",
            "Detail-oriented"
        ],
        "values_info_type": [
            "Learning outcomes",
            "Student performance metrics",
            "Training effectiveness data",
            "Curriculum development"
        ]
    },
    "RESEARCH_DEVELOPMENT": {
        "examples": ["Engineers", "scientists", "researchers"],
        "focus": "Advancing technology and innovation",
        "characteristics": [
            "Innovative mindset",
            "Highly analytical",
            "Research-oriented",
            "Technical expertise"
        ],
        "communication_style": [
            "Technical",
            "Data-driven",
            "Collaborative",
            "Detail-focused"
        ],
        "values_info_type": [
            "Research outcomes",
            "Technical specifications",
            "Project milestones",
            "Innovation metrics"
        ]
    }
}

AF_KEY_POSITIONS = {
    "FIRST_SERGEANT": {
        "title": "First Sergeant / First Shirt",
        "implied_ranks": ["E-7", "E-8"],
        "focus_areas": [
            "Quality of life",
            "Team satisfaction and dynamics",
            "Morale and welfare",
            "Personal issues resolution",
            "Discipline and standards enforcement",
            "Mentoring enlisted personnel",
            "Commander advisory role"
        ],
        "communication_style": [
            "Supportive",
            "Empathetic",
            "Direct when needed",
            "Accessible to all ranks"
        ],
        "key_responsibilities": [
            "24/7 availability for unit issues",
            "Bridge between commander and enlisted force",
            "Unit climate assessment",
            "Personnel management"
        ]
    },
    "SEL": {
        "title": "Senior Enlisted Leader",
        "implied_rank": "E-9",
        "focus_areas": [
            "Unit effectiveness",
            "Mission readiness",
            "Standards enforcement",
            "Senior enlisted mentorship",
            "Commander advisory role"
        ],
        "communication_style": [
            "Assertive",
            "Professional",
            "Strategic",
            "Experience-based"
        ],
        "key_responsibilities": [
            "Senior enlisted force development",
            "Policy implementation",
            "Strategic planning input",
            "Cross-functional leadership"
        ]
    },
    "FLIGHT_CC": {
        "title": "Flight Commander",
        "implied_rank": "O-3",
        "focus_areas": [
            "Performance of small team",
            "Peer or near-peer leadership",
            "Learning conflict resolution",
            "Mastering primary duty"
        ],
        "communication_style": [
            "Developing leadership voice",
            "Learning to balance authority with approachability",
            "Often varies based on subculture"
        ],
        "key_responsibilities": [
            "Direct leadership of flight personnel",
            "Day-to-day operations management",
            "Performance reporting",
            "Initial conflict resolution"
        ]
    },
    "SQUADRON_CC": {
        "title": "Squadron Commander",
        "implied_rank": "O-5",
        "focus_areas": [
            "Unit performance",
            "Resource management",
            "Mission readiness",
            "Personnel development",
            "Strategic planning"
        ],
        "communication_style": [
            "Authoritative",
            "Strategic",
            "Decision-focused",
            "Balance of detail and big picture"
        ],
        "key_responsibilities": [
            "Squadron mission accomplishment",
            "Resource allocation",
            "Personnel management",
            "Strategic direction",
            "Unit culture development"
        ]
    },
    "GROUP_WING_CC": {
        "title": "Group/Wing Commander",
        "implied_ranks": ["O-6", "O-7"],
        "focus_areas": [
            "Strategic direction",
            "Resource optimization",
            "Cross-unit coordination",
            "Long-term planning",
            "Higher headquarters interface"
        ],
        "communication_style": [
            "Strategic",
            "Concise",
            "Executive level",
            "Policy focused"
        ],
        "key_responsibilities": [
            "Multi-squadron oversight",
            "Strategic resource management",
            "Policy implementation",
            "Senior leader development",
            "Interface with external stakeholders"
        ]
    }
}

AF_INTERACTION_NORMS = {
    "RANK_BASED_COMMUNICATION": {
        "description": "Guidelines for communication based on rank differences",
        "principles": [
            "Communication formality increases with rank difference",
            "Peer communication is typically more casual",
            "Higher ranks may speak casually down, reverse rarely true",
            "Professional courtesies maintained regardless of familiarity"
        ],
        "exceptions": [
            "Emergency situations may reduce formality",
            "Training environments may modify norms",
            "Prior relationships may affect interaction style"
        ]
    },
    "RESPONSE_PROTOCOLS": {
        "description": "Expected patterns of response based on rank and position",
        "guidelines": [
            "Lower ranks provide concise responses to higher ranks",
            "Detail level increases when specifically requested",
            "Written communication typically more formal than verbal",
            "Chain of command considerations in communication flow"
        ],
        "context_factors": [
            "Mission urgency",
            "Setting formality",
            "Group size",
            "Presence of other ranks"
        ]
    },
    "INTERACTION_INITIATION": {
        "description": "Protocols for initiating conversations across ranks",
        "guidelines": [
            "Lower ranks typically wait to be addressed",
            "Higher ranks set tone and formality level",
            "Professional greetings always required",
            "Situational awareness affects approach"
        ],
        "exceptions": [
            "Emergency situations",
            "Safety issues",
            "Time-critical information",
            "Established mentoring relationships"
        ]
    },
    "OFF_DUTY_DYNAMICS": {
        "description": "Guidelines for non-duty interactions",
        "principles": [
            "Rank awareness persists in off-duty settings",
            "Fraternization rules always apply",
            "Professional boundaries maintained",
            "Social events may allow relaxed formality"
        ],
        "considerations": [
            "Location context",
            "Present company",
            "Type of social event",
            "Unit customs and traditions"
        ]
    },
    "MENTORSHIP_DYNAMICS": {
        "description": "Special considerations for mentoring relationships",
        "principles": [
            "More relaxed communication permitted",
            "Maintains professional boundaries",
            "Balances development with respect",
            "Considers unit dynamics"
        ],
        "special_cases": [
            "Senior NCO to Junior Officer dynamics",
            "Cross-functional mentoring",
            "Technical expert mentoring",
            "Peer mentoring"
        ]
    },
    "SITUATIONAL_AWARENESS": {
        "description": "Context-based modification of interaction norms",
        "factors": [
            "Mission requirements",
            "Location formality",
            "Present personnel",
            "Time constraints"
        ],
        "considerations": [
            "Emergency situations",
            "Training environments",
            "Formal ceremonies",
            "Operational settings"
        ]
    },
    "CULTURAL_VARIATIONS": {
        "description": "Subculture-specific interaction modifications",
        "variations": [
            "Operations tends toward direct communication",
            "Support functions more formal",
            "Technical fields more data-focused",
            "Medical more patient-oriented"
        ],
        "considerations": [
            "Unit mission type",
            "Leadership style",
            "Historical precedent",
            "Local customs"
        ]
    }
}

RESPONSE_TEMPLATES = {
    'tool_recommendation': {
        'structure': [
            "Based on what you're dealing with, I think {tool_name} would be perfect here.",
            "\nHere's why:",
            "- {context_specific_reason}",
            "- Works great for {specific_scenario}",
            "\nQuick Setup:",
            "{numbered_steps}",
            "\nCheck out the full demo here: {video_url}",
            "\nWhat are you thinking? Any specific concerns for your situation?"
        ]
    },
    'personality_guidance': {
        'structure': [
            "Ah, the classic {personality_type} situation! I've been there.",
            "\nTypically, you'll see:",
            "{bullet_point_characteristics}",
            "\nHere's what works (straight from our DTIP course):",
            "{numbered_strategies}",
            "\nWant to see this in action? {video_url}",
            "\nHow does this align with what you're seeing?"
        ]
    }
}
