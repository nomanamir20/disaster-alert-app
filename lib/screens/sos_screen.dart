import 'package:flutter/material.dart';

class SOSScreen extends StatefulWidget {
  const SOSScreen({super.key});

  @override
  State<SOSScreen> createState() => _SOSScreenState();
}

class _SOSScreenState extends State<SOSScreen> {
  bool _sosSent = false;

  void _sendSOS() {
    setState(() => _sosSent = true);
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('🚨 SOS Signal Sent! Help is on the way!'),
        backgroundColor: Colors.red,
        duration: Duration(seconds: 3),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D1B2A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF922B21),
        title: const Text('SOS Emergency',
            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
      body: SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
          children: [
            const SizedBox(height: 30),
            // SOS Button
            GestureDetector(
              onTap: _sosSent ? null : _sendSOS,
              child: Container(
                width: 200,
                height: 200,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: _sosSent ? Colors.grey : const Color(0xFF922B21),
                  boxShadow: [
                    BoxShadow(
                      color: (_sosSent ? Colors.grey : Colors.red).withOpacity(0.5),
                      blurRadius: 30,
                      spreadRadius: 10,
                    ),
                  ],
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.sos, color: Colors.white, size: 60),
                    const SizedBox(height: 8),
                    Text(
                      _sosSent ? 'SENT!' : 'PRESS',
                      style: const TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                          fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 30),
            Text(
              _sosSent
                  ? '✅ SOS sent! Rescue team notified!'
                  : 'Press the button to send emergency SOS with your GPS location',
              textAlign: TextAlign.center,
              style: TextStyle(
                  color: _sosSent ? Colors.green : Colors.white70,
                  fontSize: 16),
            ),
            const SizedBox(height: 40),
            // Emergency contacts
            const Text('Emergency Numbers',
                style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _contactCard('🚒', 'Fire Brigade', '16'),
            const SizedBox(height: 8),
            _contactCard('🚑', 'Rescue 1122', '1122'),
            const SizedBox(height: 8),
            _contactCard('🚔', 'Police', '15'),
            const SizedBox(height: 8),
            _contactCard('🏥', 'Edhi Foundation', '115'),
          ],
        ),
      ),
    );
  }

  Widget _contactCard(String emoji, String name, String number) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: const Color(0xFF1C2833),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Text(emoji, style: const TextStyle(fontSize: 24)),
          const SizedBox(width: 12),
          Expanded(
              child: Text(name,
                  style: const TextStyle(color: Colors.white, fontSize: 15))),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: const Color(0xFF922B21),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(number,
                style: const TextStyle(
                    color: Colors.white, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}