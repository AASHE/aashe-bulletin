from apps.newsletter.models import Category

categories = {
    'Academics': [
        'Curriculum',
        'Research',
    ],
    'Engagement': [
        'Campus Engagement',
        'Public Engagement',
    ],
    'Operations': [
        'Air & Climate',
        'Buildings',
        'Dining Services',
        'Energy',
        'Grounds',
        'Purchasing',
        'Transportation',
        'Waste',
        'Water',
    ],
    'Planning & Administration': [
        'Coordination, Planning & Governance',
        'Diversity & Affordability',
        'Health, Wellbeing & Work',
        'Investment',
    ],
    'Innovation': [
        'Innovation'
    ],
    'Other': [
        'Assessments & Ratings',
        'Funding',
        'Campus Sustainability in the Media',
        'Policy & Legislation'
    ]
}


def main():
    for parent_name, children_names in categories.items():
        parent_category = Category.objects.create(name=parent_name)
        for child_name in children_names:
            Category.objects.create(name=child_name,
                                    parent=parent_category)

if __name__ == '__main__':
    main()
