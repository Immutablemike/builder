import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import axios from 'axios';

interface TipButtonProps {
  creatorId: string;
  creatorName?: string;
  onTipComplete?: () => void;
}

const SUGGESTED_AMOUNTS = [1, 5, 10, 25];

export default function TipButton({
  creatorId,
  creatorName = 'Creator',
  onTipComplete
}: TipButtonProps) {
  const [showAmounts, setShowAmounts] = useState(false);
  const [customAmount, setCustomAmount] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTip = async (amount: number) => {
    setLoading(true);
    
    try {
      const response = await axios.post('/payments/checkout', {
        to_creator_id: creatorId,
        amount,
        success_url: `${window.location.origin}/tip/success`,
        cancel_url: `${window.location.origin}/tip/cancel`
      });

      if (response.data.checkout_url) {
        window.location.href = response.data.checkout_url;
      }
      
      if (onTipComplete) {
        onTipComplete();
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to process tip. Please try again.');
      console.error('Tip error:', error);
    } finally {
      setLoading(false);
      setShowAmounts(false);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={styles.tipButton}
        onPress={() => setShowAmounts(!showAmounts)}
        disabled={loading}
      >
        <Ionicons name="cash-outline" size={20} color="#ffffff" />
        <Text style={styles.tipButtonText}>
          {loading ? 'Processing...' : 'Tip Creator'}
        </Text>
      </TouchableOpacity>

      {showAmounts && (
        <View style={styles.amountsContainer}>
          <Text style={styles.amountsTitle}>
            Choose amount to tip {creatorName}:
          </Text>
          
          <View style={styles.suggestedAmounts}>
            {SUGGESTED_AMOUNTS.map((amount) => (
              <TouchableOpacity
                key={amount}
                style={styles.amountButton}
                onPress={() => handleTip(amount)}
              >
                <Text style={styles.amountButtonText}>${amount}</Text>
              </TouchableOpacity>
            ))}
          </View>

          <View style={styles.customAmountContainer}>
            <input
              style={styles.customAmountInput}
              placeholder="Custom amount"
              keyboardType="numeric"
              value={customAmount}
              onChangeText={setCustomAmount}
            />
            <TouchableOpacity
              style={styles.customAmountButton}
              onPress={() => {
                const amount = parseFloat(customAmount);
                if (amount && amount > 0) {
                  handleTip(amount);
                } else {
                  Alert.alert('Error', 'Please enter a valid amount');
                }
              }}
            >
              <Text style={styles.customAmountButtonText}>Send</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8,
  },
  tipButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#10b981',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 8,
    gap: 8,
  },
  tipButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  amountsContainer: {
    marginTop: 12,
    padding: 16,
    backgroundColor: '#f9fafb',
    borderRadius: 8,
  },
  amountsTitle: {
    fontSize: 14,
    color: '#374151',
    marginBottom: 12,
    fontWeight: '500',
  },
  suggestedAmounts: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 12,
  },
  amountButton: {
    backgroundColor: '#ffffff',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#d1d5db',
  },
  amountButtonText: {
    color: '#374151',
    fontSize: 16,
    fontWeight: '600',
  },
  customAmountContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  customAmountInput: {
    flex: 1,
    backgroundColor: '#ffffff',
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#d1d5db',
    fontSize: 16,
  },
  customAmountButton: {
    backgroundColor: '#3b82f6',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 6,
    justifyContent: 'center',
  },
  customAmountButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
});
