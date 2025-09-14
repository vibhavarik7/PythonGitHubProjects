# CAN Bus Puzzle Game 🚗⚡

A fun educational Python game that teaches CAN bus communication by controlling car subsystems through commands.

## 🎯 Overview

Control car subsystems (headlights, windows, doors, engine) using real CAN bus commands. Complete missions by sending correctly formatted messages and learn automotive communication protocols.

## 🚀 Quick Start

### Installation
```bash
pip install pygame
python main.py
```

### Basic Commands
```bash
send 0x201 01    # Turn on headlights
send 0x101 00    # Close driver window
send 0x301 01    # Lock doors
send 0x401 02    # Set engine to 2000 RPM
```

## 🎮 How to Play

1. **Study CAN Mappings**: Press SPACE to dismiss the initial mapping display
2. **Read Mission**: Current objective shown at top
3. **Enter Commands**: Use format `send 0xXXX YY` in input box
4. **Complete Missions**: Progress through 6 missions to win
5. **Learn from Errors**: Red X animation shows invalid commands

## 🔧 CAN Bus Mappings

| CAN ID | Subsystem | Data Values |
|--------|-----------|-------------|
| `0x101` | Windows | 0=Driver Close, 1=Driver Open, 2=Passenger Close, 3=Passenger Open |
| `0x201` | Headlights | 0=OFF, 1=ON |
| `0x301` | Doors | 0=UNLOCK, 1=LOCK |
| `0x401` | Engine | 0-8 (multiplied by 1000 for RPM) |

## 📁 Code Structure (Modular)

```
├── main.py           # Main game loop (155 lines)
├── constants.py      # Game constants & colors
├── enums.py          # State enumerations
├── car_state.py      # Car subsystem management
├── mission.py        # Mission system
├── can_message.py    # CAN message handling & parsing
└── ui_components.py  # All UI rendering logic
```

## 🎯 Missions

1. Turn on headlights → `send 0x201 01`
2. Close driver window → `send 0x101 00`
3. Open passenger window → `send 0x101 03`
4. Lock doors → `send 0x301 01`
5. Start engine (RPM > 1000) → `send 0x401 02`
6. Turn off headlights → `send 0x201 00`

## 🎨 Features

- **Visual Car**: Real-time subsystem state display
- **CAN Message Log**: Scrolling communication history
- **Error Animation**: Immediate feedback for wrong commands
- **Mission Progress**: Clear objectives and completion tracking
- **Mapping Display**: Reference guide (press M to toggle)

## 🔧 Controls

- **Type**: Enter CAN commands
- **ENTER**: Execute command
- **SPACE**: Dismiss mapping (at start)
- **M**: Toggle mapping display
- **BACKSPACE**: Delete input
- **ESC**: Quit game

## 🎓 Learning Objectives

- **CAN Bus Protocol**: Automotive communication standards
- **Hexadecimal Commands**: Real-world message formatting
- **System Integration**: Multi-subsystem control
- **Error Handling**: Command validation and feedback
- **Protocol Debugging**: Understanding message flow

## ⚠️ Troubleshooting

**Common Errors:**
- Wrong format → Use exact `send 0xXXX YY` syntax
- Invalid CAN ID → Only use 0x101, 0x201, 0x301, 0x401
- Bad data values → Check valid ranges per subsystem
- Case matters → Commands are case-insensitive

## 🏗️ Technical Details

- **Python 3.7+** with Pygame
- **Modular Architecture**: Clean separation of concerns
- **Type Hints**: Better code maintainability
- **60 FPS**: Smooth animations and interactions
- **Error Resilience**: Comprehensive input validation

---

**🎯 Learn CAN bus communication through hands-on practice!**