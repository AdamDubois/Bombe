/*
Fichier : Enigme2.qml
Description : Interface de l’énigme 2.

- Simule un terminal avec séquence de démarrage animée
- Affiche une progression visuelle (boot système)
- Gère l’affichage du timer
- Transition vers le module de jeu après le démarrage
*/

import QtQuick
import QtQuick.Timeline 1.0

Rectangle {
    id: root
    width: 1280
    height: 800
    color: "#0f1419"

    property int timeRemaining: 0
    property real progressValue: 0
    property bool lineAdded: false

    // ======================
    // TERMINAL LOG
    // ======================
    property string terminalLog: ""

    // Initialise le contenu du terminal
    function initTerminal() {
        clearTerminal()

        appendLine("Initialisation du système...")
        appendLine("Connexion établie")
        appendLine("Chargement du terminal...")
        appendLine("Synchronisation des modules...")
        appendLine("ANOMALIE DÉTECTÉE")
        appendLine("Accès refusé")
    }

    // Ajoute une ligne dans le terminal
    function appendLine(message) {
        terminalLog += "> " + message + "\n"
    }

    // Réinitialise le terminal
    function clearTerminal() {
        terminalLog = ""
    }

    // Convertit un temps en secondes au format MM:SS
    function formatTime(seconds) {
        var min = Math.floor(seconds / 60)
        var sec = seconds % 60

        return min.toString().padStart(2, '0') + ":" +
               sec.toString().padStart(2, '0')
    }

    // Réinitialise et relance l’animation de la timeline
    function restartAnimation() {
        timelineAnim.stop()
        timeline.currentFrame = 0

        lineAdded = false
        initTerminal()   // ← IMPORTANT

        timelineAnim.start()
    }

    // Initialise le terminal au chargement du composant
    Component.onCompleted: {
        initTerminal()
    }

    // Relance l’animation lorsque le composant devient visible
    onVisibleChanged: {
        if (visible) {
            restartAnimation()
        }
    }

    // ======================
    // UI
    // ======================
    Rectangle {
        id: rectangle
        anchors.fill: parent
        color: "transparent"
        border.width: 2
        border.color: "#27313a"

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
            x: 15
            y: 10
            text: "TERMINAL : OverClock"
            font.pixelSize: 26
            font.bold: true
            color: "#E6EDF3"
        }

        Text {
            id: text3
            x: 944
            y: 13
            text: "SYS STATUS :"
            font.pixelSize: 24
            font.bold: true
            color: "#00b4ff"
        }

        Text {
            id: text4
            x: 1116
            y: 13
            visible: true
            text: "EN LIGNE"
            font.pixelSize: 24
            font.bold: true
            color: "#00b4ff"
        }

        Rectangle {
            id: terminalWindow
            x: 320
            y: 225
            width: 639
            height: 397
            opacity: 1
            visible: false
            color: "#161C22"
            border.width: 2
            border.color: "#00b4ff"
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

        Rectangle {
            id: rectangle1
            x: 47
            y: 158
            width: 1186
            height: 603
            radius: 12

            color: "#0f1419"
            border.color: "#27313A"
            border.width: 2

            // faux effet d’ombre (simple et fiable)
            Rectangle {
                anchors.fill: parent
                anchors.margins: -4
                radius: 14
                color: "transparent"
                border.color: "#20000000"
                border.width: 4
                z: -1
            }

            Text {
                text: "MODULE DE CONTRÔLE DES TUYAUX"
                color: "#00b4ff"
                font.pixelSize: 28
                font.bold: true
            }

            Text {
                x: 23
                y: 541
                text: "Ajuster les couleurs des tuyaux pour correspondre à la séquence."
                color: "#8B949E"
                font.pixelSize: 40
            }

            Text {
                x: 0
                y: 52
                text: "SÉQUENCE REQUISE"
                color: "#00b4ff"
                font.pixelSize: 22
                font.bold: true
            }


            Row {
                spacing: 60

                anchors.centerIn: parent

                Rectangle { width: 180; height: 180; radius: 90; color: "#55007b" }
                Rectangle { width: 180; height: 180; radius: 90; color: "#0045ff" }
                Rectangle { width: 180; height: 180; radius: 90; color: "#00ff88" }
                Rectangle { width: 180; height: 180; radius: 90; color: "#fffb00" }
                Rectangle { width: 180; height: 180; radius: 90; color: "#ff7403" }
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
        font.pixelSize: 42
        font.bold: true
        font.family: "Courier New"
        visible: true
        color: "#00b4ff"
    }

    Text {
        id: bootPercent
        x: 889
        y: 648
        width: 70
        opacity: 1
        visible: false
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
            opacity: 1
            visible: true
            radius: 4
            color: "#00b4ff"
        }
    }


    Text {
        id: text2
        x: 493
        y: 129
        width: 292
        height: 52
        visible: false
        color: "#ff0000"
        text: qsTr("ACCÈS REFUSÉ")
        font.pixelSize: 45
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

                color: "#3A1A1A"
            }

            Rectangle {
                width: 70
                height: 70
                radius: 10
                border.width: 3
                border.color: "#3A3A3A"

                color: "#3A1A1A"
            }

            Rectangle {
                width: 70
                height: 70
                radius: 10
                border.width: 3
                border.color: "#3A3A3A"

                color: "#3A1A1A"
            }

            Rectangle {
                width: 70
                height: 70
                radius: 10
                border.width: 3
                border.color: "#3A3A3A"

                color: "#3A1A1A"
            }
        }

    }
    Timeline {
        id: timeline

        startFrame: 0
        endFrame: 400
        currentFrame: 0
        enabled: true

        animations: TimelineAnimation {
            id: timelineAnim
            duration: 10000
            from: 0
            to: 400
            running: true
        }

        onCurrentFrameChanged: {
            if (currentFrame >= 150 && !lineAdded) {
                appendLine("ACCÈS AU CONTRÔLE DU SYSTÈME")
                lineAdded = true
            }
        }

        KeyframeGroup {
            target: image
            property: "opacity"

            Keyframe { frame: 0; value: 1 }
            Keyframe { frame: 50; value: 1 }
            Keyframe { frame: 100; value: 0 }
        }

        KeyframeGroup {
            target: bootPercent
            property: "visible"
            Keyframe {
                value: false
                frame: 0
            }

            Keyframe {
                value: true
                frame: 100
            }

            Keyframe {
                value: false
                frame: 99
            }

            Keyframe {
                value: true
                frame: 150
            }

            Keyframe {
                value: false
                frame: 151
            }
        }

        KeyframeGroup {
            target: progressFrame
            property: "visible"
            Keyframe {
                value: false
                frame: 0
            }

            Keyframe {
                value: true
                frame: 99
            }

            Keyframe {
                value: true
                frame: 100
            }

            Keyframe {
                value: true
                frame: 100
            }

            Keyframe {
                value: false
                frame: 200
            }
        }

        KeyframeGroup {
            target: progressFrame
            property: "opacity"
            Keyframe {
                value: 1
                frame: 100
            }

            Keyframe {
                value: 0
                frame: 0
            }
        }

        KeyframeGroup {
            target: progressFill
            property: "opacity"
            Keyframe {
                value: 0
                frame: 0
            }

            Keyframe {
                value: 0
                frame: 99
            }

            Keyframe {
                value: 1
                frame: 100
            }
        }

        KeyframeGroup {
            target: root
            property: "progressValue"

            Keyframe { value: 0; frame: 0 }
            Keyframe { value: 0; frame: 99 }

            Keyframe { value: 90; frame: 100 }
            Keyframe { value: 96; frame: 123 }
            Keyframe { value: 100; frame: 150 }
        }

        KeyframeGroup {
            target: terminalWindow
            property: "opacity"
            Keyframe {
                value: 0.30202
                frame: 0
            }

            Keyframe {
                value: 0.30202
                frame: 90
            }

            Keyframe {
                value: 1
                frame: 100
            }
        }

        KeyframeGroup {
            target: terminalWindow
            property: "border.color"
            Keyframe {
                value: "#ff3b3b"
                frame: 0
            }

            Keyframe {
                value: "#ff3b3b"
                frame: 90
            }

            Keyframe {
                value: "#00b4ff"
                frame: 100
            }
        }

        KeyframeGroup {
            target: text2
            property: "visible"
            Keyframe {
                value: true
                frame: 0
            }

            Keyframe {
                value: true
                frame: 99
            }

            Keyframe {
                value: false
                frame: 100
            }
        }

        KeyframeGroup {
            target: textTimer
            property: "color"
            Keyframe {
                value: "#ff0000"
                frame: 0
            }

            Keyframe {
                value: "#ff0000"
                frame: 99
            }

            Keyframe {
                value: "#00b4ff"
                frame: 100
            }
        }

        KeyframeGroup {
            target: text3
            property: "color"
            Keyframe {
                value: "#ff0000"
                frame: 0
            }

            Keyframe {
                value: "#ff0000"
                frame: 99
            }

            Keyframe {
                value: "#00b4ff"
                frame: 100
            }
        }

        KeyframeGroup {
            target: text4
            property: "color"
            Keyframe {
                value: "#ff0000"
                frame: 0
            }

            Keyframe {
                value: "#ff0000"
                frame: 99
            }

            Keyframe {
                value: "#00b4ff"
                frame: 100
            }
        }

        KeyframeGroup {
            target: bootTerminalText
            property: "color"
            Keyframe {
                value: "#ff0000"
                frame: 0
            }

            Keyframe {
                value: "#ff0000"
                frame: 99
            }

            Keyframe {
                value: "#00b4ff"
                frame: 100
            }
        }

        KeyframeGroup {
            target: root
            property: "color"
            Keyframe {
                value: "#140d0d"
                frame: 0
            }

            Keyframe {
                value: "#140d0d"
                frame: 99
            }

            Keyframe {
                value: "#0f1419"
                frame: 100
            }
        }

        KeyframeGroup {
            target: rectangle
            property: "border.color"
            Keyframe {
                value: "#3a2727"
                frame: 0
            }

            Keyframe {
                value: "#3a2727"
                frame: 99
            }

            Keyframe {
                value: "#27313a"
                frame: 100
            }
        }

        KeyframeGroup {
            target: text4
            property: "visible"
            Keyframe {
                value: true
                frame: 0
            }

            Keyframe {
                value: true
                frame: 99
            }

            Keyframe {
                value: false
                frame: 100
            }

            Keyframe {
                value: true
                frame: 120
            }

            Keyframe {
                value: false
                frame: 140
            }

            Keyframe {
                value: true
                frame: 160
            }

            Keyframe {
                value: false
                frame: 180
            }

            Keyframe {
                value: true
                frame: 200
            }

            Keyframe {
                value: false
                frame: 220
            }

            Keyframe {
                value: true
                frame: 240
            }
        }

        KeyframeGroup {
            target: text4
            property: "text"
            Keyframe {
                value: "HORS LIGNE"
                frame: 0
            }

            Keyframe {
                value: "HORS LIGNE"
                frame: 99
            }

            Keyframe {
                value: "EN LIGNE"
                frame: 100
            }
        }

        KeyframeGroup {
            target: terminalWindow
            property: "visible"
            Keyframe {
                value: true
                frame: 199
            }

            Keyframe {
                value: false
                frame: 200
            }

            Keyframe {
                value: true
                frame: 0
            }
        }

        KeyframeGroup {
            target: rectangle1
            property: "visible"
            Keyframe {
                value: false
                frame: 0
            }

            Keyframe {
                value: true
                frame: 230
            }
        }

        KeyframeGroup {
            target: rectangle1
            property: "opacity"
            Keyframe {
                value: 0
                frame: 230
            }

            Keyframe {
                value: 1
                frame: 250
            }
        }
    }


}
