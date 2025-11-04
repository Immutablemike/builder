import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, ActivityIndicator } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';
import axios from 'axios';
import { useSupabase } from '../hooks/useSupabase';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8007';
const screenWidth = Dimensions.get('window').width;

export default function DashboardScreen() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalViews: 0,
    totalWatchTime: 0,
    totalTips: 0,
    totalComments: 0,
    totalContent: 0
  });
  const { session } = useSupabase();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/creator/dashboard`, {
        headers: {
          Authorization: `Bearer ${session?.access_token}`
        }
      });

      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center">
        <ActivityIndicator size="large" color="#3b82f6" />
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-gray-50 p-4">
      <Text className="text-3xl font-bold mb-6">Creator Dashboard</Text>

      <View className="grid grid-cols-2 gap-4 mb-6">
        <View className="bg-white p-4 rounded-lg shadow">
          <Text className="text-gray-600 text-sm">Total Views</Text>
          <Text className="text-2xl font-bold text-blue-600">
            {stats.totalViews.toLocaleString()}
          </Text>
        </View>

        <View className="bg-white p-4 rounded-lg shadow">
          <Text className="text-gray-600 text-sm">Watch Time</Text>
          <Text className="text-2xl font-bold text-green-600">
            {(stats.totalWatchTime / 3600).toFixed(1)}h
          </Text>
        </View>

        <View className="bg-white p-4 rounded-lg shadow">
          <Text className="text-gray-600 text-sm">Total Tips</Text>
          <Text className="text-2xl font-bold text-purple-600">
            ${stats.totalTips.toFixed(2)}
          </Text>
        </View>

        <View className="bg-white p-4 rounded-lg shadow">
          <Text className="text-gray-600 text-sm">Comments</Text>
          <Text className="text-2xl font-bold text-orange-600">
            {stats.totalComments}
          </Text>
        </View>
      </View>

      <View className="bg-white p-4 rounded-lg shadow mb-6">
        <Text className="text-xl font-bold mb-4">Content Overview</Text>
        <Text className="text-gray-600">
          Total Content: <Text className="font-bold">{stats.totalContent}</Text>
        </Text>
        <Text className="text-gray-600 mt-2">
          Average Views per Content:{' '}
          <Text className="font-bold">
            {stats.totalContent > 0
              ? (stats.totalViews / stats.totalContent).toFixed(0)
              : 0}
          </Text>
        </Text>
      </View>

      <View className="bg-white p-4 rounded-lg shadow">
        <Text className="text-xl font-bold mb-4">Quick Stats</Text>
        <View className="space-y-3">
          <View className="flex-row justify-between">
            <Text className="text-gray-600">Engagement Rate</Text>
            <Text className="font-semibold">
              {stats.totalViews > 0
                ? ((stats.totalComments / stats.totalViews) * 100).toFixed(1)
                : 0}
              %
            </Text>
          </View>
          <View className="flex-row justify-between">
            <Text className="text-gray-600">Avg Tip Amount</Text>
            <Text className="font-semibold">
              ${stats.totalTips > 0 ? (stats.totalTips / 10).toFixed(2) : 0}
            </Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
}
