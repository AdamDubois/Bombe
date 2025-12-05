#!/usr/bin/env python
#coding: utf-8
"""
Fichier : test_threads.py
Description: Script de test pour déterminer les capacités de threading du Raspberry Pi 4
    - Teste différents types de threads et mesure les performances
"""
__author__ = "GitHub Copilot"
__version__ = "1.0.0"
__date__ = "2025-12-05"


import threading
import time
import psutil
import multiprocessing
import sys
from concurrent.futures import ThreadPoolExecutor
import queue
import gc

class ThreadTester:
    def __init__(self):
        self.results = []
        self.active_threads = []
        self.stop_flag = threading.Event()
        
    def cpu_intensive_task(self, thread_id, duration=10):
        """Tâche CPU-intensive pour tester la charge processeur"""
        start_time = time.time()
        count = 0
        while time.time() - start_time < duration and not self.stop_flag.is_set():
            # Calcul inutile pour charger le CPU
            count += 1
            _ = sum(i**2 for i in range(100))
        return f"Thread CPU {thread_id}: {count} itérations"
    
    def io_bound_task(self, thread_id, duration=10):
        """Tâche I/O-bound similaire à votre Class_Bouton"""
        start_time = time.time()
        count = 0
        while time.time() - start_time < duration and not self.stop_flag.is_set():
            time.sleep(0.1)  # Similaire à votre Class_Bouton
            count += 1
        return f"Thread I/O {thread_id}: {count} cycles"
    
    def light_task(self, thread_id, duration=10):
        """Tâche légère avec très peu d'activité"""
        start_time = time.time()
        count = 0
        while time.time() - start_time < duration and not self.stop_flag.is_set():
            time.sleep(0.5)  # Attente plus longue
            count += 1
        return f"Thread Light {thread_id}: {count} cycles"

    def monitor_system(self, duration):
        """Monitore les ressources système pendant le test"""
        start_time = time.time()
        max_cpu = 0
        max_memory = 0
        
        while time.time() - start_time < duration and not self.stop_flag.is_set():
            cpu_percent = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()
            
            max_cpu = max(max_cpu, cpu_percent)
            max_memory = max(max_memory, memory.percent)
            
            print(f"CPU: {cpu_percent:5.1f}% | RAM: {memory.percent:5.1f}% | Threads actifs: {threading.active_count()}")
        
        return max_cpu, max_memory

    def test_thread_capacity(self, task_type="io_bound", max_threads=500, duration=10):
        """Teste la capacité maximale de threads"""
        print(f"\n=== Test de capacité: {task_type} ===")
        print(f"Cœurs CPU disponibles: {multiprocessing.cpu_count()}")
        print(f"RAM totale: {psutil.virtual_memory().total / (1024**3):.1f} GB")
        
        # Choix de la tâche
        if task_type == "cpu_intensive":
            task_func = self.cpu_intensive_task
        elif task_type == "light":
            task_func = self.light_task
        else:
            task_func = self.io_bound_task
        
        # Démarrage du monitoring
        monitor_thread = threading.Thread(
            target=self.monitor_system, 
            args=(duration,), 
            daemon=True
        )
        monitor_thread.start()
        
        threads = []
        successful_threads = 0
        
        try:
            # Création progressive des threads
            for i in range(max_threads):
                try:
                    thread = threading.Thread(
                        target=task_func,
                        args=(i, duration),
                        daemon=True
                    )
                    thread.start()
                    threads.append(thread)
                    successful_threads += 1
                    
                    # Vérification périodique
                    if i % 50 == 0 and i > 0:
                        print(f"Créé {i} threads...")
                        
                        # Vérification de la mémoire
                        memory = psutil.virtual_memory()
                        if memory.percent > 85:
                            print(f"Limite mémoire atteinte à {i} threads (RAM: {memory.percent:.1f}%)")
                            break
                            
                except Exception as e:
                    print(f"Erreur création thread {i}: {e}")
                    break
                    
            print(f"Threads créés avec succès: {successful_threads}")
            
            # Attente de la fin des tests
            time.sleep(duration)
            
        except KeyboardInterrupt:
            print("\nArrêt demandé par l'utilisateur")
            
        finally:
            # Arrêt propre
            self.stop_flag.set()
            
            # Attente de la fin des threads
            for thread in threads:
                thread.join(timeout=1.0)
            
            print(f"Test terminé. Threads actifs restants: {threading.active_count()}")
            
        return successful_threads

    def run_performance_tests(self):
        """Lance une série de tests de performance"""
        print("=== TESTS DE CAPACITÉ THREADING RASPBERRY PI 4 ===")
        
        # Test 1: Tâches I/O-bound (comme votre Class_Bouton)
        self.stop_flag.clear()
        io_capacity = self.test_thread_capacity("io_bound", max_threads=200, duration=15)
        time.sleep(2)
        
        # Test 2: Tâches légères
        self.stop_flag.clear()  
        light_capacity = self.test_thread_capacity("light", max_threads=300, duration=10)
        time.sleep(2)
        
        # Test 3: Tâches CPU-intensive
        self.stop_flag.clear()
        cpu_capacity = self.test_thread_capacity("cpu_intensive", max_threads=20, duration=10)
        
        # Résumé
        print("\n" + "="*60)
        print("RÉSULTATS FINAUX")
        print("="*60)
        print(f"Threads I/O-bound (comme Class_Bouton):  {io_capacity}")
        print(f"Threads légers:                          {light_capacity}")  
        print(f"Threads CPU-intensive:                   {cpu_capacity}")
        print("\nRECOMMANDATIONS:")
        print(f"- Votre Class_Bouton: Vous pouvez lancer jusqu'à ~{io_capacity} instances")
        print(f"- Tâches mixtes: Limitez-vous à {min(50, io_capacity//2)} threads")
        print(f"- Tâches CPU pures: Maximum {multiprocessing.cpu_count()} threads")

def main():
    print("Démarrage des tests de threading...")
    print("Appuyez sur Ctrl+C pour arrêter un test\n")
    
    tester = ThreadTester()
    
    try:
        tester.run_performance_tests()
    except KeyboardInterrupt:
        print("\nTests interrompus par l'utilisateur")
    except Exception as e:
        print(f"Erreur durant les tests: {e}")
    
    print("\nTests terminés!")

if __name__ == "__main__":
    main()