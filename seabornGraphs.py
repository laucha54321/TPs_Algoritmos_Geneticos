import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

# Define the folder for saving images and ensure it exists
output_folder = "plot_images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define a variable to add to the end of each image name
image_suffix = "20"  # Modify this variable as needed

# Load all three datasets
df_elitism = pd.read_csv('poblacion_eltisimo.csv')
df_roulette = pd.read_csv('poblacion_ruleta.csv')
df_tournament = pd.read_csv('poblacion_torneo.csv')

# Add a column to identify the selection method
df_elitism['method'] = 'Elitismo'
df_roulette['method'] = 'Ruleta'
df_tournament['method'] = 'Torneo'

# Combine all data into one DataFrame
df_combined = pd.concat([df_elitism, df_roulette, df_tournament], ignore_index=True)

# Set the style for seaborn
sns.set(style="whitegrid", palette="pastel")

#########################################
# Graph 1: Promedio de Fitness por Generación
plt.figure(figsize=(8, 6))
sns.lineplot(data=df_combined, x='gen', y='avg', hue='method', 
             ci=None, marker='o', markersize=6)
plt.title('Promedio de Fitness por Generación')
plt.xlabel('Generación')
plt.ylabel('Fitness Promedio')
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.tight_layout()
filename = os.path.join(output_folder, f"promedio_fitness_por_generacion{image_suffix}.png")
plt.savefig(filename, dpi=300)
plt.close()

#########################################
# Graph 2: Máxima Fitness por Generación
plt.figure(figsize=(8, 6))
sns.lineplot(data=df_combined, x='gen', y='max', hue='method', 
             ci=None, marker='o', markersize=6)
plt.title('Máxima Fitness por Generación')
plt.xlabel('Generación')
plt.ylabel('Fitness Máxima')
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.tight_layout()
filename = os.path.join(output_folder, f"maxima_fitness_por_generacion{image_suffix}.png")
plt.savefig(filename, dpi=300)
plt.close()

#########################################
# Graph 3: Mínima Fitness por Generación
plt.figure(figsize=(8, 6))
sns.lineplot(data=df_combined, x='gen', y='min', hue='method', 
             ci=None, marker='o', markersize=6)
plt.title('Mínima Fitness por Generación')
plt.xlabel('Generación')
plt.ylabel('Fitness Mínima')
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.tight_layout()
filename = os.path.join(output_folder, f"minima_fitness_por_generacion{image_suffix}.png")
plt.savefig(filename, dpi=300)
plt.close()

#########################################
# Graph 4: Distribución de Fitness en la Última Generación
plt.figure(figsize=(8, 6))
last_gen = df_combined[df_combined['gen'] == df_combined['gen'].max()]
sns.boxplot(data=last_gen, x='method', y='fit')
plt.title('Distribución de Fitness en la Última Generación')
plt.xlabel('Método de Selección')
plt.ylabel('Valor de Fitness')
plt.tight_layout()
filename = os.path.join(output_folder, f"distribucion_fitness_ultima_generacion{image_suffix}.png")
plt.savefig(filename, dpi=300)
plt.close()

#########################################
# Graph 5: Velocidad de Convergencia
plt.figure(figsize=(8, 6))
convergence_data = []
# Ensure the method names used in the loop match those in the DataFrame
for method in ['Elitismo', 'Ruleta', 'Torneo']:
    method_df = df_combined[df_combined['method'] == method]
    max_fitness = method_df['max'].max()
    target = 0.95 * max_fitness
    convergence_gen = method_df[method_df['max'] >= target]['gen'].min()
    convergence_data.append({'Method': method, 'Convergence Generation': convergence_gen})

convergence_df = pd.DataFrame(convergence_data)
sns.barplot(data=convergence_df, x='Method', y='Convergence Generation')
plt.title('Velocidad de Convergencia (Generación para Alcanzar 95% de Fitness Máxima)')
plt.xlabel('Método de Selección')
plt.ylabel('Generación')
plt.tight_layout()
filename = os.path.join(output_folder, f"velocidad_convergencia{image_suffix}.png")
plt.savefig(filename, dpi=300)
plt.close()

#########################################
# Graph 6: Distribución de Aptitud a través de Todas las Generaciones
# Group generations into intervals
df_combined['gen_group'] = pd.cut(df_combined['gen'], bins=20, labels=False) * 10
plt.figure(figsize=(14, 6))
sns.boxplot(data=df_combined, x='gen_group', y='fit', hue='method', dodge=True)
plt.title('Distribución de Aptitud (Agrupada en Intervalos)')
plt.xlabel('Grupo de Generaciones')
plt.ylabel('Valor de Aptitud')
plt.xticks(rotation=45)
plt.tight_layout()
filename = os.path.join(output_folder, f"fitness_distribution_all_generations{image_suffix}.png")
plt.savefig(filename, dpi=300)
plt.close()
