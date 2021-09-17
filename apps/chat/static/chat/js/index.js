let joinModal = new bootstrap.Modal(document.getElementById('joinModal'));
const input = document.getElementById('id_join-input');

function modalOpen() {
    input.value = '';
    joinModal.show();
}