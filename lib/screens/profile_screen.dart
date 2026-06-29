import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D1B2A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1A5276),
        title: const Text('Profile',
            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
      body: SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
          children: [
            const SizedBox(height: 20),
            // Profile avatar
            const CircleAvatar(
              radius: 50,
              backgroundColor: Color(0xFF1A5276),
              child: Icon(Icons.person, size: 50, color: Colors.white),
            ),
            const SizedBox(height: 12),
            const Text('User Name',
                style: TextStyle(
                    color: Colors.white,
                    fontSize: 22,
                    fontWeight: FontWeight.bold)),
            const Text('Lahore, Pakistan',
                style: TextStyle(color: Colors.white54)),
            const SizedBox(height: 30),
            // Settings
            _settingItem(Icons.location_on, 'My Location', 'Lahore, Punjab'),
            _settingItem(Icons.notifications, 'Alert Notifications', 'Enabled'),
            _settingItem(Icons.language, 'Language', 'English / اردو'),
            _settingItem(Icons.contacts, 'Emergency Contacts', '3 contacts'),
            _settingItem(Icons.shield, 'Safety Tips', 'View all tips'),
            _settingItem(Icons.info, 'About App', 'Version 1.0.0'),
          ],
        ),
      ),
    );
  }

  Widget _settingItem(IconData icon, String title, String subtitle) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xFF1C2833),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Icon(icon, color: const Color(0xFF5DADE2), size: 22),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title,
                    style: const TextStyle(
                        color: Colors.white, fontWeight: FontWeight.bold)),
                Text(subtitle,
                    style: const TextStyle(
                        color: Colors.white54, fontSize: 12)),
              ],
            ),
          ),
          const Icon(Icons.arrow_forward_ios, color: Colors.white38, size: 14),
        ],
      ),
    );
  }
}