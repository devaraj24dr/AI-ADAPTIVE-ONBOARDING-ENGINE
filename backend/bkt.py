# ============================================================
#  TENSOR TITANS — AI Adaptive Onboarding Engine
#  Module      : Mastery Tracking Engine
#  Description : Tracks learner progress using Knowledge Tracing
#  Team        : TENSOR TITANS
# ============================================================


# ---------- Default Probability Constants ----------

INITIAL_MASTERY   = 0.30   # How much learner knows at start
LEARNING_RATE     = 0.20   # How fast they learn each attempt
GUESS_PROBABILITY = 0.25   # Chance of lucky guess
SLIP_PROBABILITY  = 0.10   # Chance of silly mistake


# ---------- Mastery Tracker ----------

class SkillTracker:
    """
    Tracks mastery level of a single skill.
    Updates based on quiz results using
    Bayesian Knowledge Tracing logic.
    """

    def __init__(self, skill_name):
        self.skill      = skill_name
        self.mastery    = INITIAL_MASTERY
        self.attempts   = 0
        self.history    = []

    def update(self, answered_correct: bool):
        """
        Call this after every quiz attempt.
        Pass True if correct, False if wrong.
        """
        self.attempts += 1

        if answered_correct:
            # Correct answer → boost mastery
            p_correct = (
                self.mastery * (1 - SLIP_PROBABILITY) +
                (1 - self.mastery) * GUESS_PROBABILITY
            )
            self.mastery = (
                self.mastery * (1 - SLIP_PROBABILITY)
            ) / p_correct

        else:
            # Wrong answer → reduce mastery
            p_wrong = (
                self.mastery * SLIP_PROBABILITY +
                (1 - self.mastery) * (1 - GUESS_PROBABILITY)
            )
            self.mastery = (
                self.mastery * SLIP_PROBABILITY
            ) / p_wrong

        # Apply learning effect
        self.mastery = self.mastery + (1 - self.mastery) * LEARNING_RATE
        self.mastery = round(min(max(self.mastery, 0.0), 1.0), 4)

        self.history.append({
            "attempt" : self.attempts,
            "correct" : answered_correct,
            "mastery" : self.mastery
        })

        print(f"[TENSOR TITANS] {self.skill} mastery: {self.mastery * 100:.1f}%")
        return self.mastery

    def is_mastered(self, threshold=0.80):
        """Returns True if learner has mastered this skill."""
        return self.mastery >= threshold

    def summary(self):
        """Returns a full summary of this skill's progress."""
        return {
            "skill"     : self.skill,
            "mastery"   : self.mastery,
            "attempts"  : self.attempts,
            "mastered"  : self.is_mastered(),
            "history"   : self.history
        }


# ---------- Multi Skill Session ----------

class LearnerSession:
    """
    Manages mastery tracking across
    multiple skills for one learner.
    """

    def __init__(self, learner_name):
        self.learner  = learner_name
        self.trackers = {}

    def record(self, skill, correct: bool):
        """Record a quiz result for a specific skill."""
        if skill not in self.trackers:
            self.trackers[skill] = SkillTracker(skill)
        return self.trackers[skill].update(correct)

    def get_weak_skills(self):
        """Returns skills where mastery is still below 80%."""
        return [
            s for s, t in self.trackers.items()
            if not t.is_mastered()
        ]

    def full_report(self):
        """Returns complete progress report for this learner."""
        return {
            "learner" : self.learner,
            "skills"  : {
                s: t.summary()
                for s, t in self.trackers.items()
            }
        }