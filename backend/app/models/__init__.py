"""
SQLModel models for AI-Powered Quran Coach
"""

from .sessions import Session, SessionCreate, SessionRead, SessionUpdate
from .insights import Insight, InsightCreate, InsightRead, InsightUpdate
from .mistakes import Mistake, MistakeCreate, MistakeRead, MistakeUpdate
from .portion_details import PortionDetail, PortionDetailCreate, PortionDetailRead, PortionDetailUpdate
from .test_types import TestType, TestTypeCreate, TestTypeRead, TestTypeUpdate
from .learning_methods import LearningMethod, LearningMethodCreate, LearningMethodRead, LearningMethodUpdate

__all__ = [
    "Session", "SessionCreate", "SessionRead", "SessionUpdate",
    "Insight", "InsightCreate", "InsightRead", "InsightUpdate", 
    "Mistake", "MistakeCreate", "MistakeRead", "MistakeUpdate",
    "PortionDetail", "PortionDetailCreate", "PortionDetailRead", "PortionDetailUpdate",
    "TestType", "TestTypeCreate", "TestTypeRead", "TestTypeUpdate",
    "LearningMethod", "LearningMethodCreate", "LearningMethodRead", "LearningMethodUpdate"
] 