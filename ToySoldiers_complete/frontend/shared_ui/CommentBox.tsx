import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, input, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import axios from 'axios';
import { useSupabase } from '../hooks/useSupabase';

interface Comment {
  id: string;
  user_id: string;
  text: string;
  created_at: string;
  parent_id?: string;
  user?: {
    email: string;
  };
}

interface CommentBoxProps {
  contentId: string;
  onCommentAdded?: () => void;
}

export default function CommentBox({ contentId, onCommentAdded }: CommentBoxProps) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const { session } = useSupabase();

  useEffect(() => {
    fetchComments();
  }, [contentId]);

  const fetchComments = async () => {
    try {
      const response = await axios.get(`/chat/comments/${contentId}`);
      setComments(response.data);
    } catch (error) {
      console.error('Failed to fetch comments:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitComment = async () => {
    if (!newComment.trim() || !session) {
      return;
    }

    setSubmitting(true);

    try {
      await axios.post(
        '/chat/comment',
        {
          content_id: contentId,
          text: newComment
        },
        {
          headers: {
            Authorization: `Bearer ${session.access_token}`
          }
        }
      );

      setNewComment('');
      fetchComments();
      
      if (onCommentAdded) {
        onCommentAdded();
      }
    } catch (error) {
      console.error('Failed to submit comment:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const renderComment = ({ item }: { item: Comment }) => (
    <View style={styles.commentContainer}>
      <View style={styles.commentHeader}>
        <Text style={styles.commentAuthor}>
          {item.user?.email || 'Anonymous'}
        </Text>
        <Text style={styles.commentDate}>
          {new Date(item.created_at).toLocaleDateString()}
        </Text>
      </View>
      <Text style={styles.commentText}>{item.text}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        Comments ({comments.length})
      </Text>

      {session && (
        <View style={styles.inputContainer}>
          <input
            style={styles.input}
            placeholder="Add a comment..."
            value={newComment}
            onChangeText={setNewComment}
            multiline
            numberOfLines={3}
          />
          <TouchableOpacity
            style={[
              styles.submitButton,
              (!newComment.trim() || submitting) && styles.submitButtonDisabled
            ]}
            onPress={handleSubmitComment}
            disabled={!newComment.trim() || submitting}
          >
            <Ionicons
              name="send"
              size={20}
              color={!newComment.trim() || submitting ? '#9ca3af' : '#ffffff'}
            />
          </TouchableOpacity>
        </View>
      )}

      {loading ? (
        <Text style={styles.loadingText}>Loading comments...</Text>
      ) : comments.length === 0 ? (
        <Text style={styles.emptyText}>
          No comments yet. Be the first to comment!
        </Text>
      ) : (
        <FlatList
          data={comments}
          renderItem={renderComment}
          keyExtractor={(item) => item.id}
          style={styles.commentsList}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    padding: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#333',
  },
  inputContainer: {
    flexDirection: 'row',
    marginBottom: 16,
    gap: 8,
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#d1d5db',
    borderRadius: 8,
    padding: 12,
    fontSize: 14,
    textAlignVertical: 'top',
  },
  submitButton: {
    backgroundColor: '#3b82f6',
    width: 44,
    height: 44,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  submitButtonDisabled: {
    backgroundColor: '#e5e7eb',
  },
  commentsList: {
    flex: 1,
  },
  commentContainer: {
    marginBottom: 16,
    padding: 12,
    backgroundColor: '#f9fafb',
    borderRadius: 8,
  },
  commentHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  commentAuthor: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
  },
  commentDate: {
    fontSize: 12,
    color: '#6b7280',
  },
  commentText: {
    fontSize: 14,
    color: '#4b5563',
    lineHeight: 20,
  },
  loadingText: {
    textAlign: 'center',
    color: '#6b7280',
    padding: 20,
  },
  emptyText: {
    textAlign: 'center',
    color: '#9ca3af',
    padding: 40,
    fontSize: 14,
  },
});
