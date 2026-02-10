import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, TextInput, View, Alert } from 'react-native';
import { fetchEmergencyContacts } from '../api/safety';
import { SectionCard } from '../components/SectionCard';
import { colors, spacing, typography } from '../theme-soft';

type Contact = {
  id: number;
  name: string;
  phone_number: string;
  relationship: string;
  priority: number;
};

export function ProfileScreen() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [status, setStatus] = useState('Syncing...');

  useEffect(() => {
    let isMounted = true;
    fetchEmergencyContacts()
      .then((data) => {
        if (isMounted) {
          setContacts(data);
          setStatus(data.length ? 'Synced' : 'No contacts');
        }
      })
      .catch((error) => {
        if (isMounted) {
          setStatus(`Offline`);
          console.error("Profile Contact Fetch Error:", error);
          Alert.alert("Sync Error", `Could not load contacts.\n${error.message}`);
        }
      });
    return () => { isMounted = false; };
  }, []);

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.header}>My Profile</Text>

      <SectionCard title="Personal Details">
        <View style={styles.field}>
          <Text style={styles.label}>Full Name</Text>
          <TextInput placeholder="Enter your name" style={styles.input} placeholderTextColor="#BDBDBD" />
        </View>
        <View style={styles.field}>
          <Text style={styles.label}>Phone Number</Text>
          <TextInput placeholder="+91 98765 43210" style={styles.input} placeholderTextColor="#BDBDBD" />
        </View>
        <View style={styles.field}>
          <Text style={styles.label}>University / Campus</Text>
          <TextInput placeholder="Main Campus" style={styles.input} placeholderTextColor="#BDBDBD" />
        </View>
      </SectionCard>

      <SectionCard title="Emergency Contacts" subtitle={status}>
        {contacts.length ? (
          contacts.map((contact) => (
            <View key={contact.id} style={styles.contactRow}>
              <View style={styles.avatar}>
                <Text style={styles.avatarText}>{contact.name[0]}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.contactName}>{contact.name}</Text>
                <Text style={styles.contactMeta}>
                  {contact.relationship} • {contact.phone_number}
                </Text>
              </View>
            </View>
          ))
        ) : (
          <Text style={styles.bodyText}>Add trusted contacts to keep them informed.</Text>
        )}
      </SectionCard>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: spacing.lg,
    paddingTop: 60,
    gap: spacing.lg,
    backgroundColor: colors.background,
    paddingBottom: 100,
  },
  header: {
    ...typography.header,
    marginBottom: spacing.xs,
  },
  field: {
    marginBottom: spacing.md,
  },
  label: {
    ...typography.caption,
    color: colors.textSecondary,
    marginBottom: 6,
  },
  input: {
    backgroundColor: '#F5F5F5',
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: spacing.md,
    color: colors.text,
    fontSize: 16,
  },
  contactRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#FFEAA7',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  avatarText: {
    color: '#FDCB6E',
    fontWeight: '700',
    fontSize: 18,
  },
  contactName: {
    ...typography.title,
    fontSize: 16,
  },
  contactMeta: {
    ...typography.caption,
    marginTop: 2,
  },
  bodyText: {
    ...typography.body,
    fontStyle: 'italic',
    color: '#BDBDBD',
  },
});
