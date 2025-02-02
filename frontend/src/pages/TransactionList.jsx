import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTransactions, deleteTransaction } from '../services/TransactionService/transactionService';

const TransactionList = () => {
    const [transactions, setTransactions] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchTransactions();
    }, []);

    const fetchTransactions = async () => {
        try {
            const data = await getTransactions();
            setTransactions(data);
        } catch (error) {
            console.error('Failed to fetch transactions');
        }
    };

    const handleDelete = async (id) => {
        try {
            await deleteTransaction(id);
            fetchTransactions();
        } catch (error) {
            console.error('Failed to delete transaction');
        }
    };

    return (
        <div style={{ textAlign: 'center' }}>
            <h2>Transactions</h2>
            <button onClick={() => navigate('/transactions/new')} style={{ marginBottom: '20px' }}>Add New Transaction</button>
            <ul>
                {transactions.map((transaction) => (
                    <li key={transaction.id}>
                        {transaction.heading} - {transaction.description} - ${transaction.amount}
                        <button onClick={() => navigate(`/transactions/edit/${transaction.id}`)}>Edit</button>
                        <button onClick={() => handleDelete(transaction.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TransactionList;