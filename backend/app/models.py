"""
HARV SHIPPED - Unified Database Models
Combines models from Steel2, Doc Digester, and Harv
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


# ============================================================================
# USER MANAGEMENT (from Harv)
# ============================================================================

class User(Base):
    """User accounts for students and administrators."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Onboarding data (stored as JSON)
    learning_style = Column(String(50))  # visual, auditory, kinesthetic, etc.
    familiarity = Column(String(50))  # beginner, intermediate, advanced
    goals = Column(Text)
    background = Column(Text)

    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    progress = relationship("UserProgress", back_populates="user")
    memory_summaries = relationship("MemorySummary", back_populates="user")


# ============================================================================
# CURRICULUM MODULES (from Steel2 + Harv)
# ============================================================================

class Module(Base):
    """
    Teaching modules (converted from Steel2 weeks).
    Represents one week of Latin A curriculum.
    """
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    week_number = Column(Integer, unique=True, nullable=False)  # 1-35
    title = Column(String(500), nullable=False)
    description = Column(Text)

    # Prompts (from Steel2)
    system_prompt = Column(Text)  # Socratic teaching instructions
    module_prompt = Column(Text)  # Specific learning objectives

    # Knowledge base
    system_corpus = Column(Text)  # Core knowledge (grammar, vocabulary)
    module_corpus = Column(Text)  # Examples, exercises, activities

    # Metadata (from Steel2 week_spec)
    grammar_focus = Column(String(500))
    virtue = Column(String(100))
    faith_phrase = Column(String(500))
    learning_objectives = Column(JSON)  # Array of objectives

    # Status
    is_published = Column(Boolean, default=False)
    quality_score = Column(Float)  # From validation
    last_validated = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    conversations = relationship("Conversation", back_populates="module")
    progress = relationship("UserProgress", back_populates="module")
    memory_summaries = relationship("MemorySummary", back_populates="module")


# ============================================================================
# CONVERSATIONS & LEARNING (from Harv)
# ============================================================================

class Conversation(Base):
    """Student conversations with AI tutor."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)

    # Chat history (stored as JSON array)
    messages_json = Column(Text, nullable=False, default="[]")

    # Progress tracking
    current_grade = Column(String(10))  # A+, A, B+, etc.
    finalized = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
    module = relationship("Module", back_populates="conversations")


class UserProgress(Base):
    """Student progress per module."""
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)

    # Completion status
    completed = Column(Boolean, default=False)
    grade = Column(String(10))  # Final grade
    time_spent = Column(Integer, default=0)  # Minutes
    attempts = Column(Integer, default=0)
    completion_date = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="progress")
    module = relationship("Module", back_populates="progress")


class MemorySummary(Base):
    """Learning insights extracted from conversations."""
    __tablename__ = "memory_summaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)

    # Learning insights
    what_learned = Column(Text)
    how_learned = Column(Text)
    key_concepts = Column(Text)
    learning_insights = Column(Text)
    teaching_effectiveness = Column(Text)
    understanding_level = Column(String(50))  # beginner, proficient, advanced

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="memory_summaries")
    module = relationship("Module", back_populates="memory_summaries")


# ============================================================================
# PATTERN LIBRARY (from Doc Digester integration)
# ============================================================================

class PatternLibrary(Base):
    """
    Pedagogical patterns extracted from Doc Digester analyses.
    Used to inform Steel2 curriculum generation.
    """
    __tablename__ = "pattern_library"

    id = Column(Integer, primary_key=True, index=True)
    source_chapter_id = Column(String(100), index=True)  # From Doc Digester analysis
    pattern_type = Column(String(50), nullable=False)  # lesson_flow, assessment, teaching_strategy, etc.

    # Pattern data (stored as JSON)
    pattern_data = Column(JSON, nullable=False)

    # Metadata
    frequency = Column(Integer, default=1)  # How often this pattern appears
    quality_rating = Column(Float)  # 0.0 - 1.0
    source_metadata = Column(JSON)  # Original analysis metadata

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================
# QUALITY REPORTS (NEW for HARV SHIPPED)
# ============================================================================

class QualityReport(Base):
    """Quality validation reports for curriculum weeks."""
    __tablename__ = "quality_reports"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    week_number = Column(Integer, nullable=False)

    # Quality metrics
    quality_score = Column(Float, nullable=False)  # 0-10
    structural_coherence = Column(Float)
    pedagogical_soundness = Column(Float)
    concept_clarity = Column(Float)
    assessment_alignment = Column(Float)
    spiral_learning_coverage = Column(Float)  # 0.0 - 1.0

    # Issues and recommendations (stored as JSON)
    issues = Column(JSON)
    recommendations = Column(JSON)

    # Validation metadata
    validator = Column(String(50), default="doc_digester")
    validated_at = Column(DateTime, default=datetime.utcnow)


# ============================================================================
# FEEDBACK ANALYSES (NEW for HARV SHIPPED)
# ============================================================================

class FeedbackAnalysis(Base):
    """Student performance analysis for curriculum improvement."""
    __tablename__ = "feedback_analyses"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)

    # Performance metrics
    student_count = Column(Integer, nullable=False)
    completion_rate = Column(Float)
    average_grade = Column(String(10))
    average_time_minutes = Column(Float)
    median_time_minutes = Column(Float)

    # Issues (stored as JSON)
    common_misconceptions = Column(JSON)
    struggling_concepts = Column(JSON)
    successful_strategies = Column(JSON)

    # Recommendations (stored as JSON)
    improvement_recommendations = Column(JSON)

    # Analysis metadata
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    needs_refinement = Column(Boolean, default=False)
