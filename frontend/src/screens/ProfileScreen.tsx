import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { fetchEmergencyContacts } from '../api/safety';
import { SectionCard } from '../components/SectionCard';
import { colors, spacing, typography } from '../theme';

type Contact = {
  id: number;
  name: string;
  phone_number: string;
  relationship: string;
  priority: number;
};

export function ProfileScreen() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [status, setStatus] = useState('Loading contacts...');

  useEffect(() => {
    let isMounted = true;
    fetchEmergencyContacts()
      .then((data) => {
        if (isMounted) {
          setContacts(data);
          setStatus(data.length ? 'Active contacts loaded.' : 'No contacts found.');
        }
      })
      .catch((error) => {
        if (isMounted) {
          setStatus(`API not connected: ${error.message}`);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Profile</Text>

      <SectionCard title="Personal Info" subtitle="Update your safety profile">
        <View style={styles.field}>
          <Text style={styles.label}>Name</Text>
          <TextInput placeholder="Student name" style={styles.input} placeholderTextColor={colors.muted} />
        </View>
        <View style={styles.field}>
          <Text style={styles.label}>Phone</Text>
          <TextInput placeholder="+91 98765 43210" style={styles.input} placeholderTextColor={colors.muted} />
        </View>
        <View style={styles.field}>
          <Text style={styles.label}>Campus</Text>
          <TextInput placeholder="Main campus" style={styles.input} placeholderTextColor={colors.muted} />
        </View>
      </SectionCard>

      <SectionCard title="Emergency Contacts" subtitle={status}>
        {contacts.length ? (
          contacts.map((contact) => (
            <View key={contact.id} style={styles.contactRow}>
              <Text style={styles.contactName}>{contact.name}</Text>
              <Text style={styles.contactMeta}>
                {contact.relationship || 'Contact'} • {contact.phone_number}
              </Text>
            </View>
          ))
        ) : (
          <Text style={styles.bodyText}>Add contacts once authentication is enabled.</Text>
        )}
      </SectionCard>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: spacing.lg,
    gap: spacing.md,
    backgroundColor: colors.background,
  },
  title: {
    color: colors.text,
    ...typography.title,
  },
  field: {
    marginBottom: spacing.sm,
  },
  label: {
    color: colors.muted,
    ...typography.label,
  },
  input: {
    marginTop: spacing.xs,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 12,
    paddingVertical: spacing.xs,
    paddingHorizontal: spacing.sm,
    color: colors.text,
    backgroundColor: '#fff',
  },
  contactRow: {
    paddingVertical: spacing.xs,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  contactName: {
    color: colors.text,
    ...typography.subtitle,
  },
  contactMeta: {
    color: colors.muted,
    ...typography.body,
  },
  bodyText: {
    color: colors.muted,
    ...typography.body,
  },
});
