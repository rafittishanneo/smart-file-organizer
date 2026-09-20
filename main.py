from controllers.organizer_controller import FileOrganizerController
from models.organizer_model import FileOrganizerModel
from views.organizer_view import FileOrganizerView


def main() -> None:
    model = FileOrganizerModel()
    view = FileOrganizerView()
    FileOrganizerController(model, view)
    view.mainloop()


if __name__ == "__main__":
    main()
