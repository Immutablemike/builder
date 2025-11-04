import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, Image, ActivityIndicator } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import axios from 'axios';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8004';

export default function HomeFeed() {
  const [content, setContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const navigation = useNavigation();

  useEffect(() => {
    fetchFeed();
  }, []);

  const fetchFeed = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/content/feed`, {
        params: {
          limit: 20,
          offset: 0,
          visibility: 'public'
        }
      });

      setContent(response.data);
    } catch (error) {
      console.error('Failed to fetch feed:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    fetchFeed();
  };

  const renderContentItem = ({ item }) => (
    <TouchableOpacity
      onPress={() => navigation.navigate('Player', { contentId: item.id })}
      className="bg-white mb-4 rounded-lg shadow-md overflow-hidden"
    >
      {item.thumbnail_url && (
        <Image
          source={{ uri: item.thumbnail_url }}
          className="w-full h-48"
          resizeMode="cover"
        />
      )}
      <View className="p-4">
        <Text className="text-lg font-bold mb-2">{item.title}</Text>
        {item.description && (
          <Text className="text-gray-600 mb-2" numberOfLines={2}>
            {item.description}
          </Text>
        )}
        <View className="flex-row flex-wrap">
          {item.tags && item.tags.map((tag, index) => (
            <View key={index} className="bg-blue-100 px-2 py-1 rounded mr-2 mb-2">
              <Text className="text-blue-600 text-sm">{tag}</Text>
            </View>
          ))}
        </View>
        <Text className="text-gray-500 text-sm mt-2">
          {new Date(item.created_at).toLocaleDateString()}
        </Text>
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-gray-50">
        <ActivityIndicator size="large" color="#3b82f6" />
      </View>
    );
  }

  return (
    <View className="flex-1 bg-gray-50">
      <View className="bg-white p-4 shadow-sm">
        <Text className="text-2xl font-bold">Discover</Text>
      </View>
      <FlatList
        data={content}
        renderItem={renderContentItem}
        keyExtractor={(item) => item.id}
        contentContainerStyle={{ padding: 16 }}
        refreshing={refreshing}
        onRefresh={handleRefresh}
        ListEmptyComponent={
          <View className="flex-1 justify-center items-center py-20">
            <Text className="text-gray-500 text-lg">No content available</Text>
          </View>
        }
      />
    </View>
  );
}
