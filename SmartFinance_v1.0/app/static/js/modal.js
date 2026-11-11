document.addEventListener('DOMContentLoaded', () => {
    // отримуємо елементі модал
    const modal = document.getElementById('transactionModal');
    const btn = document.getElementById('openModal');
    const span = document.querySelector('.modal .close');
    const typeRadios = document.querySelectorAll('input[name="type"]');
    const categorySelect = document.querySelector('select[name="category"]');
    const emotionDiv = document.querySelector('.emotion');

    
     const categories = {
        income: ['Зарплата', 'Бізнес', 'Подарунки', 'Інше'],
        expense: ['Їжа', 'Транспорт', 'Одяг', 'Подарунки', 'Техніка', 'Розваги', 'Освіта', 'Здоров\'я', 'Дім/Комунальні', 'Інше']
    };

    function updateForm(type) {

        categorySelect.innerHTML = '';

        categories[type].forEach(cat => {
            const option = document.createElement('option');
            option.textContent = cat;
            option.value = cat;
            categorySelect.appendChild(option);
        });

        if (type === 'expense') {
            emotionDiv.style.display = 'block';
        } else {
            emotionDiv.style.display = 'none';
        }
    }

    if (btn) {
        btn.onclick = () => {
            modal.style.display = 'flex';
            document.querySelector('input[value="income"]').checked = true;
            updateForm('income');
        };
    }

    if (span) {
        span.onclick = () => {
            modal.style.display = 'none';
        };
    }



window.addEventListener('click', function(event) {

    const transactionModal = document.getElementById('transactionModal');
    const editModal = document.getElementById('editModal');

    if (event.target === transactionModal) {
        transactionModal.style.display = 'none';
    }

    if (event.target === editModal) {
        editModal.style.display = 'none';
    }

});

  // зміна типу транз
    typeRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            updateForm(e.target.value);
        });
    });
});


// модал редагування
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {

      const editTypeRadios = document.querySelectorAll('#editModal input[name="type"]');

    
    function updateEditForm(type) {
        const categorySelect = document.getElementById('edit_category');
        const emotionDiv = document.querySelector('#editModal .emotion');

        const categories = {
            income: ['Зарплата', 'Бізнес', 'Подарунки', 'Інше'],
            expense: ['Їжа', 'Транспорт', 'Одяг', 'Подарунки', 'Техніка', 'Розваги', 'Освіта', 'Здоров\'я', 'Дім/Комунальні', 'Інше']
        };

       
        categorySelect.innerHTML = '';

        categories[type].forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            categorySelect.appendChild(option);
        });

     
        if (type === 'expense') {
            emotionDiv.style.display = 'block';
        } else {
            emotionDiv.style.display = 'none';

            const emotionSelect = document.getElementById('edit_emotion');
            if (emotionSelect) emotionSelect.value = '';
        }
    }

    
    editTypeRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            updateEditForm(e.target.value);
        });
    });

   
    window.openEditModal = function (id, type, amount, category, emotion, description) {

        const modal = document.getElementById('editModal');
        const form = document.getElementById('editForm');

        form.action = `/transaction/edit/${id}/`;

        document.getElementById('edit_amount').value = amount;
        document.getElementById('edit_description').value = description;

       
        const typeRadios = document.querySelectorAll('#editModal input[name="type"]');
        typeRadios.forEach(r => {
            r.checked = (r.value === type);
        });

        updateEditForm(type);

        
        requestAnimationFrame(() => {
            const categoryEl = document.getElementById('edit_category');
            const emotionEl = document.getElementById('edit_emotion');

            if (categoryEl) categoryEl.value = category;
            if (emotionEl) emotionEl.value = emotion;
        });

        modal.style.display = 'flex';
    };

});


function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}