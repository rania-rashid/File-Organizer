from file_organizer_automation import get_file_category , organize_files

def test_get_file_category_images():
    assert get_file_category(".jpg") == "Images"

def test_get_file_category_unknown():
    assert get_file_category(".xyz") == "Others"
def test_organize_files_moves_file(tmp_path):
    # Arrange: create one dummy file inside the fresh temp folder
    dummy_file = tmp_path / "photo.jpg"
    dummy_file.touch()

    # Act: run the real function against it
    organize_files(tmp_path)

    # Assert: the file should no longer be sitting at its original spot
    assert not dummy_file.exists()
import datetime

def test_organize_files_moves_to_correct_folder(tmp_path):
    dummy_file = tmp_path / "photo.jpg"
    dummy_file.touch()

    organize_files(tmp_path)

    now = datetime.datetime.now()
    expected_folder = f"{now.year}-{now.strftime('%B')}"
    expected_path = tmp_path / "Images" / expected_folder / "photo.jpg"

    assert expected_path.exists()