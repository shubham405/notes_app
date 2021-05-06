  
function delete_note(noteId) {
    fetch("/delete-note", {
      method: 'POST',
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }