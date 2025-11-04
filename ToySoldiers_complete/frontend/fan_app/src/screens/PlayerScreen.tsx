import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { Video, Audio } from 'expo-av';
import { Ionicons } from '@expo/vector-icons';
import axios from 'axios';
import { useRoute } from '@react-navigation/native';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8004';

export default function PlayerScreen() {
  const route = useRoute();
  const { contentId } = route.params;
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);
  const videoRef = useRef(null);

  useEffect(() => {
    fetchContent();
    trackView();
  }, [contentId]);

  const fetchContent = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/content/${contentId}`);
      setContent(response.data);
    } catch (error) {
      Alert.alert('Error', 'Failed to load content');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const trackView = async () => {
    try {
      await axios.post(`${BACKEND_URL}/content/analytics/view`, {
        content_id: contentId,
        device_type: 'mobile'
      });
    } catch (error) {
      console.error('Failed to track view:', error);
    }
  };

  const togglePlayPause = async () => {
    if (videoRef.current) {
      if (isPlaying) {
        await videoRef.current.pauseAsync();
      } else {
        await videoRef.current.playAsync();
      }
      setIsPlaying(!isPlaying);
    }
  };

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-black">
        <ActivityIndicator size="large" color="#ffffff" />
      </View>
    );
  }

  if (!content) {
    return (
      <View className="flex-1 justify-center items-center bg-black">
        <Text className="text-white text-lg">Content not found</Text>
      </View>
    );
  }

  const isVideo = content.media_url?.includes('video') || content.stream_url?.includes('video');

  return (
    <View className="flex-1 bg-black">
      {isVideo ? (
        <Video
          ref={videoRef}
          source={{ uri: content.stream_url || content.media_url }}
          className="flex-1"
          useNativeControls
          resizeMode="contain"
          onPlaybackStatusUpdate={(status) => {
            if (status.isLoaded) {
              setIsPlaying(status.isPlaying);
            }
          }}
        />
      ) : (
        <View className="flex-1 justify-center items-center">
          <TouchableOpacity
            onPress={togglePlayPause}
            className="bg-white rounded-full p-8"
          >
            <Ionicons
              name={isPlaying ? 'pause' : 'play'}
              size={64}
              color="#000"
            />
          </TouchableOpacity>
        </View>
      )}

      <View className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4">
        <Text className="text-white text-2xl font-bold mb-2">
          {content.title}
        </Text>
        {content.description && (
          <Text className="text-gray-300 mb-2">{content.description}</Text>
        )}
        <View className="flex-row flex-wrap">
          {content.tags && content.tags.map((tag, index) => (
            <View key={index} className="bg-blue-600 px-3 py-1 rounded mr-2 mb-2">
              <Text className="text-white text-sm">{tag}</Text>
            </View>
          ))}
        </View>
      </View>
    </View>
  );
}
