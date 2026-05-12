/*
Fichier : Enigme3.qml
Description : Interface de l’énigme 3.

- Affiche une transition entre deux écrans (animation)
- Présente le module de contrôle puis le module de désamorçage
- Gère l’affichage du timer
*/

import QtQuick
import QtQuick.Timeline 1.0

Rectangle {
    id: root
    width: 1280
    height: 800
    color: "#0f1419"

    property int timeRemaining: 0

    // Convertit un temps en secondes au format MM:SS
    function formatTime(seconds) {
        var min = Math.floor(seconds / 60)
        var sec = seconds % 60
        return min.toString().padStart(2, "0") + ":" +
               sec.toString().padStart(2, "0")
    }

    // Réinitialise la timeline et relance l’animation depuis le début
    function restartAnimation() {
        timelineAnim.stop()
        timeline.currentFrame = 0
        timelineAnim.start()
    }

    // Relance l’animation lorsque le composant devient visible
    onVisibleChanged: {
        if (visible) {
            restartAnimation()
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
            id: rectangle1
            x: 47
            y: 158
            width: 1186
            height: 603
            radius: 12
            opacity: 1

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

        Rectangle {
            id: rectangle2
            x: 47
            y: 158
            width: 1186
            height: 603
            radius: 12
            opacity: 1
            visible: true

            color: "#0f1419"
            border.color: "#27313A"
            border.width: 2

            Column {
                x: 20
                y: 10
                spacing: 6

                Text {
                    text: "MODULE DE DÉSAMORÇAGE"
                    color: "#00b4ff"
                    font.pixelSize: 34
                    font.bold: true
                }

                Rectangle {
                    width: 300
                    height: 2
                    color: "#00b4ff"
                    opacity: 0.6
                }

                Text {
                    text: "Une séquence est requise pour désamorcer le module"
                    color: "#8B949E"
                    font.pixelSize: 40
                    wrapMode: Text.WordWrap
                }
            }

            Image {
                id: rond_code
                x: 948
                y: 237
                source: "images/rond_code.png"
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: deuxLignes
                x: 635
                y: 151
                source: "images/deuxLignes.png"
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: interogtion_code
                x: 304
                y: 298
                source: "images/interogtion_code.png"
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: genredeS_code
                x: 65
                y: 130
                source: "images/genredeS_code.png"
                fillMode: Image.PreserveAspectFit
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
            duration: 8000
            from: 0
            to: 400
            running: false
        }

        // rectangle1 visible au début
        KeyframeGroup {
            target: rectangle1
            property: "visible"

            Keyframe { frame: 0; value: true }
        }

        // fade out après ~3 secondes
        KeyframeGroup {
            target: rectangle1
            property: "opacity"

            Keyframe { frame: 0; value: 1 }
            Keyframe { frame: 40; value: 1 }
            Keyframe { frame: 70; value: 0 }
        }

        // disparition complète après le fade
        KeyframeGroup {
            target: rectangle1
            property: "visible"

            Keyframe { frame: 0; value: true }
            Keyframe { frame: 40; value: true }
            Keyframe { frame: 70; value: false }
        }

        KeyframeGroup {
            target: rectangle2
            property: "visible"
            Keyframe {
                value: false
                frame: 0
            }

            Keyframe {
                value: false
                frame: 90
            }

            Keyframe {
                value: true
                frame: 91
            }
        }

        KeyframeGroup {
            target: rectangle2
            property: "opacity"
            Keyframe {
                value: 0
                frame: 0
            }

            Keyframe {
                value: 0
                frame: 91
            }

            Keyframe {
                value: 1
                frame: 120
            }
        }
    }

}
