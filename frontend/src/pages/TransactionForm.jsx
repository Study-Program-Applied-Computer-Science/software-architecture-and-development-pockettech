import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createTransaction, updateTransaction, getTransactions } from '../services/TransactionService/transactionService';

const TransactionForm = ({ onTransactionCreated }) => {
    const { transactionId } = useParams();
    const navigate = useNavigate();
    const [alertMessage, setAlertMessage] = useState('');
    const [formData, setFormData] = useState({
        recording_user_id: '',
        credit_user_id: '',
        debit_user_id: '',
        other_party: '',
        heading: '',
        description: '',
        transaction_mode: '',
        shared_transaction: false,
        category: 0,
        amount: 0,
        currency_code: 0
    });

    useEffect(() => {
        if (transactionId) {
            fetchTransaction(transactionId);
        }
    }, [transactionId]);

    const fetchTransaction = async (id) => {
        try {
            const transactions = await getTransactions();
            const transaction = transactions.find(t => t.id === id);
            if (transaction) setFormData(transaction);
        } catch (error) {
            console.error('Error fetching transaction:', error);
        }
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]: type === 'checkbox' ? checked : value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (transactionId) {
                await updateTransaction(transactionId, formData);
                setAlertMessage('Transaction updated successfully!');
            } else {
                await createTransaction(formData);
                setAlertMessage('Transaction added successfully!');
            }
            onTransactionCreated();
            setTimeout(() => {
                setAlertMessage('');
                navigate('/transactions');
            }, 2000);
        } catch (error) {
            console.error('Error saving transaction');
        }
    };

    return (
        <div>
            <button onClick={() => navigate('/transactions')} style={{ marginTop: '20px' }}>Back</button>
            <h2>{transactionId ? 'Edit Transaction' : 'Add a Transaction'}</h2>
            {alertMessage && <div style={{ color: 'green', marginBottom: '10px' }}>{alertMessage}</div>}
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', maxWidth: '400px', margin: 'auto' }}>
                {Object.keys(formData).map((key) => (
                    <label key={key} style={{ marginBottom: '10px' }}>
                        {key.replace(/_/g, ' ').toUpperCase()}:
                        {typeof formData[key] === 'boolean' ? (
                            <input type="checkbox" name={key} checked={formData[key]} onChange={handleChange} />
                        ) : (
                            <input type={typeof formData[key] === 'number' ? 'number' : 'text'} name={key} value={formData[key]} onChange={handleChange} required={!(key === 'description' || key === 'credit_user_id' || key === 'debit_user_id' || key === 'other_party')} />
                        )}
                    </label>
                ))}
                <button type="submit" style={{ marginTop: '10px' }}>{transactionId ? 'Update' : 'Add'} Transaction</button>
            </form>
        </div>
    );
};

export default TransactionForm;