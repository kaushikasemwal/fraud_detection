async function detectFraud() {
    const transaction = {
        transaction_id: document.getElementById("transaction_id").value,
        payer_id: document.getElementById("payer_id").value,
        payee_id: document.getElementById("payee_id").value,
        amount: parseFloat(document.getElementById("amount").value),
        channel: document.getElementById("channel").value,
        mode: document.getElementById("mode").value,
        bank_code: document.getElementById("bank_code").value,
        transaction_datetime: new Date().toISOString()
    };

    const response = await fetch('http://127.0.0.1:8000/api/v1/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(transaction),
    });
    const result = await response.json();

    // Display the result
    document.getElementById("result").innerHTML = `
        <p>Transaction ID: ${result.transaction_id}</p>
        <p>Is Fraud Predicted: ${result.is_fraud_predicted}</p>
        <p>Fraud Score: ${result.fraud_score.toFixed(2)}</p>
        <p>Message: ${result.message}</p>
    `;
}
