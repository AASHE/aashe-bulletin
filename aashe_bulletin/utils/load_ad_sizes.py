"""Load initial ad sizes into bulletin db.
"""
from bulletin.models import AdSize


def main():

    AdSize.objects.create(name="Full Banner",
                          width=468,
                          height=60)


if __name__ == "__main__":
    main()
