import 'package:flutter/material.dart';

class MapScreen extends StatelessWidget {
  const MapScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D1B2A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1A5276),
        title: const Text('Disaster Map',
            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
      body: Stack(
        children: [
          // Map placeholder
          Container(
            width: double.infinity,
            height: double.infinity,
            color: const Color(0xFF1C2833),
            child: const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.map, color: Colors.white24, size: 80),
                  SizedBox(height: 16),
                  Text('Google Maps will load here',
                      style: TextStyle(color: Colors.white54)),
                  Text('(Google Maps API integration — Day 8)',
                      style: TextStyle(color: Colors.white38, fontSize: 12)),
                ],
              ),
            ),
          ),
          // Legend
          Positioned(
            bottom: 20,
            left: 16,
            right: 16,
            child: Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFF1A5276).withOpacity(0.95),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Map Legend',
                      style: TextStyle(
                          color: Colors.white, fontWeight: FontWeight.bold)),
                  SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _legendItem(Colors.red, 'Emergency'),
                      _legendItem(Colors.orange, 'Warning'),
                      _legendItem(Colors.yellow, 'Watch'),
                      _legendItem(Colors.green, 'Safe'),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _legendItem extends StatelessWidget {
  final Color color;
  final String label;
  const _legendItem(this.color, this.label);

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
            width: 12, height: 12,
            decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
        const SizedBox(width: 4),
        Text(label, style: const TextStyle(color: Colors.white70, fontSize: 11)),
      ],
    );
  }
}