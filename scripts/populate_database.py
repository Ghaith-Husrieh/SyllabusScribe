"""
Run this script using the following command:
python manage.py runscript -v3 populate_database
-v2 and -v3 are optional and are used for verbose outputs
This script populates the database with sample data using Factory Boy factories.
"""

from Base.factories import (LessonContextFactory, LessonHandoutFactory,
                            LessonPlanFactory, LessonPresentationFactory,
                            LessonQuizFactory, SubjectFactory, UnitFactory,
                            UserFactory)
from Base.models import User


def run():
    """
    Populates the database with sample data using Factory Boy factories.
    """
    pass
