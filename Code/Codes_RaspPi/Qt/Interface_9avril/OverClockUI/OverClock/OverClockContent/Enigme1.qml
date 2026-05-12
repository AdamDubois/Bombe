/*
Fichier : Enigme1.qml
Description : Interface de l’énigme 1.

- Affiche une séquence de démarrage animée (boot)
- Simule un terminal avec progression et messages
- Gère l’état des capteurs RFID
- Affiche le timer du jeu
*/

import QtQuick
import QtQuick.Controls
import QtQuick.Timeline 1.0

Rectangle {
    id: root
    width: 1280
    height: 800
    color: "#140d0d"

    property real offlineOpacity: 0.0
    property real terminalOpacity: 0.0
    property real progressValue: 0
    property string terminalLog: ""
    property int lastMessageStep: -1

    //Gestion du timer
    property int timeRemaining: 0

    //Gestion des variables partagées
    property int enigme: 0
    property var rfidState: [false, false, false, false]

    // boot similé
    function bootMessage(value) {
        if (value < 20)
            return "Initialisation des modules système..."
        else if (value < 40)
            return "Vérification des connexions..."
        else if (value < 60)
            return "Chargement du terminal..."
        else if (value < 80)
            return "Synchronisation des modules..."
        else if (value < 89)
            return "ANOMALIE DÉTECTÉE — tentative d'accès non autorisée"
        else if (value < 100)
            return "Finalisation du démarrage..."
        else
            return "Système prêt."
    }

    // Ajoute un message de démarrage (boot) dans le terminal en fonction de la progression
    function appendBootMessage(value) {
        var step = -1

        if (value < 1)
            step = -1
        else if (value < 20)
            step = 0
        else if (value < 40)
            step = 1
        else if (value < 60)
            step = 2
        else if (value < 80)
            step = 3
        else if (value < 100)
            step = 4
        else
            step = 5

        if (step !== -1 && step !== lastMessageStep) {
            lastMessageStep = step
            terminalLog += "> " + bootMessage(value) + "\n"
        }
    }

    // Convertit un temps en secondes au format MM:SS
    function formatTime(seconds) {
        var min = Math.floor(seconds / 60)
        var sec = seconds % 60
        return min.toString().padStart(2, "0") + ":" +
                sec.toString().padStart(2, "0")
    }

    // Réinitialise et relance l’animation lorsque l’écran devient visible
    onVisibleChanged: {
        if (visible) {
            terminalLog = ""
            lastMessageStep = -1

            timelineAnimation.stop()
            timeline.currentFrame = timeline.startFrame
            timelineAnimation.start()
        }
    }

    // Met à jour le terminal en fonction de la progression
    onProgressValueChanged: {
        appendBootMessage(progressValue)
    }

    Rectangle {
        id: rectangle
        anchors.fill: parent
        color: "transparent"
        border.width: 2
        border.color: "#3a2727"

        Rectangle {
            x: 10
            y: 10
            width: 911
            height: 40
            color: "#161C22"
            border.color: "#27313A"
            border.width: 1
        }

        Rectangle {
            x: 933
            y: 10
            width: 337
            height: 40
            color: "#161C22"
            border.color: "#27313A"
            border.width: 1
        }

        Text {
            id: terminalTitle
            x: 15
            y: 10
            width: 277
            height: 40
            text: "TERMINAL : OverClock"
            font.pixelSize: 26
            font.bold: true
            color: "#E6EDF3"
        }

        Text {
            id: sysText
            x: 944
            y: 13
            width: 147
            height: 34
            visible: true
            text: "SYS STATUS :"
            font.pixelSize: 24
            font.bold: true
            color: "#ff0000"
        }

        Text {
            id: offlineText
            x: 1116
            y: 13
            width: 141
            height: 37
            text: "HORS LIGNE"
            font.pixelSize: 24
            font.bold: true
            color: "#ff0000"
            visible: false
        }

        Item {
            id: terminalGroup
            opacity: 1

            Rectangle {
                id: terminalWindow
                x: 320
                y: 225
                width: 639
                height: 397
                opacity: 1
                color: "#161C22"
                border.width: 2
                border.color: "#ff3b3b"
                radius: 6

                Text {
                    id: bootTerminalText
                    anchors.fill: parent
                    anchors.margins: 16

                    text: root.terminalLog
                    color: "#ff0000"
                    font.pixelSize: 18
                    font.family: "Courier New"

                    wrapMode: Text.Wrap
                    verticalAlignment: Text.AlignTop
                    horizontalAlignment: Text.AlignLeft
                }
            }


            Image {
                id: image
                x: 0
                y: 25
                width: 1278
                height: 796
                visible: true
                source: "images/CadenasRouge.png"
                fillMode: Image.PreserveAspectFit

                Text {
                    id: text1
                    x: 344
                    y: 590
                    width: 591
                    height: 77
                    color: "#ff0000"
                    text: qsTr("Confirmation de l’identité requise")
                    font.pixelSize: 40
                }


                Row {
                    anchors.horizontalCenter: parent.horizontalCenter
                    y: 673
                    spacing: 40   // distance entre les cases

                    Rectangle {
                        width: 70
                        height: 70
                        radius: 10
                        border.width: 3
                        border.color: "#3A3A3A"

                        color: root.rfidState[0] ? "#1E7A3A" : "#111821"
                    }

                    Rectangle {
                        width: 70
                        height: 70
                        radius: 10
                        border.width: 3
                        border.color: "#3A3A3A"

                        color: root.rfidState[1] ? "#1E7A3A" : "#111821"
                    }

                    Rectangle {
                        width: 70
                        height: 70
                        radius: 10
                        border.width: 3
                        border.color: "#3A3A3A"

                        color: root.rfidState[2] ? "#1E7A3A" : "#111821"
                    }

                    Rectangle {
                        width: 70
                        height: 70
                        radius: 10
                        border.width: 3
                        border.color: "#3A3A3A"

                        color: root.rfidState[3] ? "#1E7A3A" : "#111821"
                    }
                }

                Text {
                    id: text3
                    x: 386
                    y: 644
                    width: 55
                    height: 38
                    color: "#ff0000"
                    text: qsTr("1+2")
                    font.pixelSize: 30
                }

                Text {
                    id: text4
                    x: 537
                    y: 734
                    width: 55
                    height: 38
                    color: "#ff0000"
                    text: qsTr("4+5")
                    font.pixelSize: 30
                }

                Text {
                    id: text5
                    x: 678
                    y: 638
                    width: 55
                    height: 38
                    color: "#ff0000"
                    text: qsTr("2x2")
                    font.pixelSize: 30
                }

                Text {
                    id: text6
                    x: 825
                    y: 734
                    width: 55
                    height: 38
                    color: "#ff0000"
                    text: qsTr("7/7")
                    font.pixelSize: 30
                }
            }

            Text {
                id: text2
                x: 493
                y: 129
                width: 292
                height: 52
                visible: true
                color: "#ff0000"
                text: qsTr("ACCÈS REFUSÉ")
                font.pixelSize: 45
            }

            Rectangle {
                id: terminalScreen
                x: 336
                y: 240
                width: 608
                height: 367
                opacity: 0
                color: "#000000"
                radius: 4
            }

            Text {
                id: bootLabel
                x: 321
                y: 648
                opacity: 1
                visible: false
                text: "SYSTEM BOOT"
                color: "#8B949E"
                font.pixelSize: 16
                font.bold: true
            }

            Text {
                id: bootPercent
                x: 889
                y: 648
                width: 70
                opacity: 1
                visible: true
                color: "#00b4ff"
                horizontalAlignment: Text.AlignRight
                text: Math.round(root.progressValue) + "%"
                font.pixelSize: 16
                font.bold: true
            }

            Rectangle {
                id: progressFrame
                x: 321
                y: 680
                width: 638
                height: 24
                opacity: 0
                visible: false
                radius: 4
                color: "#161C22"
                border.width: 1
                border.color: "#27313A"

                Rectangle {
                    id: progressFill
                    width: (root.progressValue / 100) * progressFrame.width
                    height: parent.height
                    opacity: 0
                    visible: true
                    radius: 4
                    color: "#ff0000"
                }

            }




        }
    }

    Text {
        id: textTimer
        x: 40
        y: 100
        width: 220
        height: 80
        text: root.formatTime(root.timeRemaining)
        color: root.timeRemaining <= 60 ? "#ff0000" : "#ff3b3b"
        font.pixelSize: 42
        font.bold: true
        font.family: "Courier New"
        visible: true
    }


    // Cette timeline gère l’ensemble des animations
    Timeline {
        id: timeline
        enabled: true
        startFrame: 0
        endFrame: 2000

        animations: [
            TimelineAnimation {
                id: timelineAnimation
                from: 0
                to: 1200
                duration: 10000
                running: false
                loops: 1
            }
        ]

        KeyframeGroup {
            target: offlineText
            property: "visible"
            Keyframe {
                value: true
                frame: 146
            }

            Keyframe {
                value: false
                frame: 177
            }

            Keyframe {
                value: true
                frame: 206
            }

            Keyframe {
                value: false
                frame: 236
            }

            Keyframe {
                value: true
                frame: 266
            }
        }

        KeyframeGroup {
            target: terminalWindow
            property: "opacity"
            Keyframe {
                value: 0
                frame: 145
            }

            Keyframe {
                value: 1
                frame: 195
            }

            Keyframe {
                value: 0.30202
                frame: 1041
            }

            Keyframe {
                value: 1
                frame: 1037
            }

            Keyframe {
                value: 0
                frame: 0
            }
        }

        KeyframeGroup {
            target: progressFrame
            property: "visible"

            Keyframe { frame: 0; value: false }
            Keyframe { frame: 156; value: false }
            Keyframe { frame: 195; value: true }

            Keyframe {
                value: true
                frame: 1040
            }

            Keyframe {
                value: false
                frame: 1041
            }
        }

        KeyframeGroup {
            target: progressFrame
            property: "opacity"

            Keyframe { frame: 0; value: 0 }
            Keyframe { frame: 156; value: 0 }
            Keyframe { frame: 195; value: 1 }
        }

        KeyframeGroup {
            target: bootLabel
            property: "visible"
            Keyframe {
                value: true
                frame: 156
            }

            Keyframe {
                value: true
                frame: 1040
            }

            Keyframe {
                value: false
                frame: 1041
            }
        }

        KeyframeGroup {
            target: bootLabel
            property: "opacity"
            Keyframe {
                value: 0
                frame: 0
            }

            Keyframe {
                value: 0
                frame: 157
            }

            Keyframe {
                value: 1
                frame: 196
            }
        }

        KeyframeGroup {
            target: bootPercent
            property: "opacity"
            Keyframe {
                value: 0
                frame: 160
            }

            Keyframe {
                value: 1
                frame: 200
            }

            Keyframe {
                value: 0
                frame: 0
            }
        }

        KeyframeGroup {
            target: root
            property: "progressValue"

            Keyframe {
                value: 0
                frame: 171
            }
            Keyframe {
                value: 0
                frame: 250
            }

            Keyframe {
                value: 1
                frame: 251
            }

            Keyframe {
                value: 5
                frame: 551
            }

            Keyframe {
                value: 12
                frame: 621
            }

            Keyframe {
                value: 22
                frame: 681
            }

            Keyframe {
                value: 38
                frame: 741
            }

            Keyframe {
                value: 55
                frame: 801
            }

            Keyframe {
                value: 68
                frame: 861
            }

            Keyframe {
                value: 78
                frame: 921
            }

            Keyframe {
                value: 84
                frame: 981
            }

            Keyframe {
                value: 90
                frame: 1040
            }

        }

        KeyframeGroup {
            target: progressFill
            property: "opacity"
            Keyframe {
                value: 0
                frame: 171
            }

            Keyframe {
                value: 1
                frame: 251
            }

            Keyframe {
                value: 0
                frame: 0
            }
        }

        KeyframeGroup {
            target: terminalWindow
            property: "border.color"
            Keyframe {
                value: "#ff3b3b"
                frame: 1040
            }

            Keyframe {
                value: "#00b4ff"
                frame: 1030
            }

            Keyframe {
                value: "#ff3b3b"
                frame: 1037
            }

            Keyframe {
                value: "#00b4ff"
                frame: 0
            }
        }

        KeyframeGroup {
            target: bootTerminalText
            property: "color"

            Keyframe { value: "#00b4ff"; frame: 0 }
            Keyframe { value: "#00b4ff"; frame: 1037 }
            Keyframe { value: "#ff0000"; frame: 1038 }
        }

        KeyframeGroup {
            target: sysText
            property: "color"
            Keyframe {
                value: "#00b4ff"
                frame: 0
            }

            Keyframe {
                value: "#00b4ff"
                frame: 1039
            }

            Keyframe {
                value: "#ff0000"
                frame: 1040
            }
        }

        KeyframeGroup {
            target: offlineText
            property: "color"
            Keyframe {
                value: "#00b4ff"
                frame: 0
            }

            Keyframe {
                value: "#00b4ff"
                frame: 1039
            }

            Keyframe {
                value: "#ff0000"
                frame: 1040
            }
        }

        KeyframeGroup {
            target: bootPercent
            property: "color"
            Keyframe {
                value: "#00b4ff"
                frame: 0
            }

            Keyframe {
                value: "#00b4ff"
                frame: 1039
            }

            Keyframe {
                value: "0"
                frame: 1041
            }
        }

        KeyframeGroup {
            target: progressFill
            property: "color"
            Keyframe {
                value: "#00b4ff"
                frame: 0
            }

            Keyframe {
                value: "#00b4ff"
                frame: 1039
            }

            Keyframe {
                value: "#ff0000"
                frame: 1040
            }
        }

        KeyframeGroup {
            target: rectangle
            property: "border.color"
            Keyframe {
                value: "#27313a"
                frame: 0
            }

            Keyframe {
                value: "#27313a"
                frame: 1039
            }

            Keyframe {
                value: "#3a2727"
                frame: 1040
            }
        }

        KeyframeGroup {
            target: root
            property: "color"
            Keyframe {
                value: "#0f1419"
                frame: 0
            }

            Keyframe {
                value: "#0f1419"
                frame: 1039
            }

            Keyframe {
                value: "#140d0d"
                frame: 1040
            }
        }

        KeyframeGroup {
            target: image
            property: "visible"
            Keyframe {
                value: false
                frame: 1040
            }

            Keyframe {
                value: false
                frame: 0
            }

            Keyframe {
                value: true
                frame: 1041
            }
        }

        KeyframeGroup {
            target: progressFill
            property: "visible"
            Keyframe {
                value: true
                frame: 1040
            }

            Keyframe {
                value: false
                frame: 1041
            }

            Keyframe {
                value: true
                frame: 0
            }
        }

        KeyframeGroup {
            target: bootPercent
            property: "visible"
            Keyframe {
                value: true
                frame: 1040
            }

            Keyframe {
                value: false
                frame: 1041
            }

            Keyframe {
                value: true
                frame: 0
            }

            Keyframe {
                value: true
                frame: 160
            }
        }

        KeyframeGroup {
            target: textTimer
            property: "visible"
            Keyframe {
                value: false
                frame: 0
            }

            Keyframe {
                value: false
                frame: 1040
            }

            Keyframe {
                value: true
                frame: 1041
            }
        }

        KeyframeGroup {
            target: text2
            property: "visible"
            Keyframe {
                value: false
                frame: 0
            }

            Keyframe {
                value: false
                frame: 1040
            }

            Keyframe {
                value: true
                frame: 1041
            }
        }

    }
}
