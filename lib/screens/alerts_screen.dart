import 'package:flutter/material.dart';

class AlertsScreen extends StatelessWidget {
  const AlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D1B2A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1A5276),
        title: const Text('Active Alerts',
            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _alertCard('🌊', 'FLOOD WARNING', 'Sindh Province — River levels critical',
              'Evacuate low-lying areas immediately', Colors.red, '10 min ago'),
          const SizedBox(height: 12),
          _alertCard('🌍', 'EARTHQUAKE WATCH', 'Balochistan — Magnitude 4.2',
              'Stay away from buildings. Move to open areas', Colors.orange, '2 hrs ago'),
          const SizedBox(height: 12),
          _alertCard('🌪️', 'STORM WARNING', 'Karachi Coastal Area',
              'Strong winds expected. Secure loose objects', Colors.orange, '5 hrs ago'),
          const SizedBox(height: 12),
          _alertCard('🔥', 'WILDFIRE ALERT', 'KPK Northern Region',
              'Fire spreading. Avoid area completely', Colors.red, '1 day ago'),
        ],
      ),
    );
  }

  Widget _alertCard(String emoji, String title, String subtitle,
      String action, Color color, String time) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1C2833),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color, width: 1.5),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(emoji, style: const TextStyle(fontSize: 28)),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title,
                        style: TextStyle(
                            color: color,
                            fontWeight: FontWeight.bold,
                            fontSize: 14)),
                    Text(subtitle,
                        style: const TextStyle(
                            color: Colors.white, fontSize: 13)),
                  ],
                ),
              ),
              Text(time,
                  style: const TextStyle(color: Colors.white54, fontSize: 11)),
            ],
          ),
          const SizedBox(height: 10),
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: color.withOpacity(0.15),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              children: [
                Icon(Icons.info_outline, color: color, size: 16),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(action,
                      style: TextStyle(color: color, fontSize: 12)),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}