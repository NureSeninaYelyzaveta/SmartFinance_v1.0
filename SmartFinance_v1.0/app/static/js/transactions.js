document.addEventListener('DOMContentLoaded', () => {
    const transactions = [];   
    let balance = 0;

    const transactionList = document.querySelector('.transaction-list') || createTransactionList();
    const balanceEl = document.getElementById('balance');
    const noTransactions = document.querySelector('.no-transactions');

    const addBtn = document.getElementById('addTransactionBtn');
    const modal = document.getElementById('transactionModal');

    addBtn.addEventListener('click', () => {
        const type = modal.querySelector('input[name="type"]:checked')?.value;
        const amount = parseFloat(modal.querySelector('input[name="amount"]').value);
        const category = modal.querySelector('select[name="category"]').value;
        const description = modal.querySelector('input[name="description"]').value;
        const date = new Date().toLocaleDateString();

        if (!type || !amount || isNaN(amount)) {
            alert('Введіть всі дані');
            return;
        }

        if (noTransactions) {
noTransactions.style.display = 'none';
 }


        const transaction = { type, amount, category, description, date };
        transactions.push(transaction);

        balance += type === 'income' ? amount : -amount;
        balanceEl.textContent = balance + '₴';

        const div = document.createElement('div');
        div.className = `transaction-item ${type}`;
        div.innerHTML = `
            <div class="transaction-date">${date}</div>
            <div class="transaction-type">${type === 'income' ? 'Дохід' : 'Витрата'}</div>
            <div class="transaction-category">${category}</div>
            <div class="transaction-amount">${amount}₴</div>
            <div class="transaction-description">${description}</div>
        `;
        transactionList.appendChild(div);

       
        modal.querySelector('input[name="amount"]').value = '';
        modal.querySelector('input[name="description"]').value = '';
        modal.querySelector('input[name="type"]:checked').checked = false;
        modal.querySelector('select[name="category"]').selectedIndex = 0;
    });

   
    function createTransactionList() {
        const section = document.querySelector('.transactions');
        const div = document.createElement('div');
        div.className = 'transaction-list';
        section.insertBefore(div, section.querySelector('#openModal'));
        return div;
    }
});