import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView, ActivityIndicator, Alert } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import { Video } from 'expo-av';
import axios from 'axios';
import { useSupabase } from '../hooks/useSupabase';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8004';

export default function UploadScreen() {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [tags, setTags] = useState('');
  const [visibility, setVisibility] = useState('public');
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const { session } = useSupabase();

  const pickFile = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['video/*', 'audio/*'],
        copyToCacheDirectory: true
      });

      if (result.type === 'success') {
        setFile(result);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to pick file');
      console.error(error);
    }
  };

  const uploadContent = async () => {
    if (!file || !title) {
      Alert.alert('Error', 'Please select a file and enter a title');
      return;
    }

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', {
        uri: file.uri,
        type: file.mimeType,
        name: file.name
      });
      formData.append('title', title);
      formData.append('description', description);
      formData.append('tags', tags);
      formData.append('visibility', visibility);

      const response = await axios.post(
        `${BACKEND_URL}/content/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${session?.access_token}`
          },
          onUploadProgress: (progressEvent) => {
            const progress = (progressEvent.loaded / progressEvent.total) * 100;
            setUploadProgress(progress);
          }
        }
      );

      Alert.alert('Success', 'Content uploaded successfully!');
      
      setFile(null);
      setTitle('');
      setDescription('');
      setTags('');
      setUploadProgress(0);
    } catch (error) {
      Alert.alert('Error', 'Failed to upload content');
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <ScrollView className="flex-1 bg-white p-4">
      <Text className="text-2xl font-bold mb-6">Upload Content</Text>

      <TouchableOpacity
        onPress={pickFile}
        className="bg-blue-500 p-4 rounded-lg mb-4"
      >
        <Text className="text-white text-center font-semibold">
          {file ? `Selected: ${file.name}` : 'Pick Audio/Video File'}
        </Text>
      </TouchableOpacity>

      <View className="mb-4">
        <Text className="text-gray-700 mb-2">Title *</Text>
        <input
          className="border border-gray-300 p-3 rounded-lg"
          value={title}
          onChangeText={setTitle}
          placeholder="Enter content title"
        />
      </View>

      <View className="mb-4">
        <Text className="text-gray-700 mb-2">Description</Text>
        <textarea
          className="border border-gray-300 p-3 rounded-lg"
          value={description}
          onChangeText={setDescription}
          placeholder="Enter content description"
          multiline
          numberOfLines={4}
        />
      </View>

      <View className="mb-4">
        <Text className="text-gray-700 mb-2">Tags (comma-separated)</Text>
        <input
          className="border border-gray-300 p-3 rounded-lg"
          value={tags}
          onChangeText={setTags}
          placeholder="e.g., music, beats, lofi"
        />
      </View>

      <View className="mb-4">
        <Text className="text-gray-700 mb-2">Visibility</Text>
        <View className="flex-row space-x-2">
          {['public', 'unlisted', 'private'].map((vis) => (
            <TouchableOpacity
              key={vis}
              onPress={() => setVisibility(vis)}
              className={`flex-1 p-3 rounded-lg ${
                visibility === vis ? 'bg-blue-500' : 'bg-gray-200'
              }`}
            >
              <Text
                className={`text-center capitalize ${
                  visibility === vis ? 'text-white' : 'text-gray-700'
                }`}
              >
                {vis}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {uploading && (
        <View className="mb-4">
          <Text className="text-gray-700 mb-2">
            Uploading: {uploadProgress.toFixed(0)}%
          </Text>
          <View className="bg-gray-200 rounded-full h-2">
            <View
              className="bg-blue-500 h-2 rounded-full"
              style={{ width: `${uploadProgress}%` }}
            />
          </View>
        </View>
      )}

      <TouchableOpacity
        onPress={uploadContent}
        disabled={uploading || !file || !title}
        className={`p-4 rounded-lg ${
          uploading || !file || !title ? 'bg-gray-400' : 'bg-green-500'
        }`}
      >
        {uploading ? (
          <ActivityIndicator color="white" />
        ) : (
          <Text className="text-white text-center font-semibold text-lg">
            Upload Content
          </Text>
        )}
      </TouchableOpacity>
    </ScrollView>
  );
}
