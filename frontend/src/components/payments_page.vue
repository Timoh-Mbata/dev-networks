<template>
  <div class="payment-container">
    <form @submit.prevent="submitMac" class="payment-form">
      <h2>Enter Your Device MAC Address</h2>
      <input 
        v-model="macAddress" 
        placeholder="e.g. AB:CD:EF:12:34:56" 
        required
      />

      <h2>Enter Phone Number</h2>
      <input 
        v-model="phoneNumber" 
        placeholder="e.g. +1234567890" 
        required
      />
      <h2>Amount</h2>
      <input 
        v-model="amount" 
        placeholder="10" 
        required
      />

      <button type="submit">Submit</button>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      macAddress: "",
      phoneNumber: "",
      amount:"",
      errorMessage: "",
    };
  },
  methods: {
    async submitMac() {
      if (!this.macAddress || !this.phoneNumber || !this.amount) {
        this.errorMessage = "Please enter both MAC address and phone number.";
        return;
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/pay", {
          mac_address: this.macAddress,
          phone_number: this.phoneNumber,
          amount:this.amount,
        });

        alert(response.data.message);
        this.errorMessage = "";
      } catch (error) {
        this.errorMessage = "Payment failed. Try again.";
      }
    },
  },
};
</script>

<style scoped>
/* Container Styling */
.payment-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f4f4;
}

/* Form Styling */
.payment-form {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 300px;
}

/* Input Styling */
input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

/* Button Styling */
button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  width: 100%;
}

button:hover {
  background-color: #218838;
}

/* Error Message */
.error-message {
  color: red;
  margin-top: 10px;
}
</style>
