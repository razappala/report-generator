// Datos de ejemplo (normalmente estos vendrían de una API o un archivo JSON)
const data = {
  resumen_evaluacion: {
    porcentaje_cumplimiento_global: 80,
    total_respuestas: {
      si: 80,
      no: 20,
    },
    procesos: [
      { nombre: "Gestión de Proyectos", porcentaje: 80 },
      { nombre: "Gestión de Riesgos", porcentaje: 85 },
      { nombre: "Seguridad de la Información", porcentaje: 75 },
      { nombre: "Continuidad del Negocio", porcentaje: 70 },
      { nombre: "Cumplimiento", porcentaje: 90 },
    ],
  },
  procesos: [
    {
      nombre: "Gestión de Proyectos",
      porcentaje_cumplimiento: 80,
      preguntas_evaluadas: 20,
      preguntas_no_cumplidas: 4,
      recomendaciones: [
        "Mejorar la documentación de los proyectos",
        "Implementar un sistema de seguimiento automatizado",
      ],
      actividades: [
        {
          nombre: "Planificación de Proyectos",
          porcentaje_cumplimiento: 85,
          tareas: [
            {
              nombre: "Revisar el Statement of Work",
              porcentaje_cumplimiento: 90,
            },
            {
              nombre: "Definir instrucciones de entrega",
              porcentaje_cumplimiento: 80,
            },
          ],
        },
        {
          nombre: "Ejecución del Plan del Proyecto",
          porcentaje_cumplimiento: 78,
          tareas: [
            {
              nombre: "Monitorear ejecución y registrar datos",
              porcentaje_cumplimiento: 80,
            },
          ],
        },
      ],
    },
    // Aquí irían los demás procesos...
  ],
};

// Función para crear el gráfico de dona
function crearGraficoDona() {
  const ctx = document.getElementById("grafico-dona").getContext("2d");
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Cumplimiento", "No Cumplimiento"],
      datasets: [
        {
          data: [
            data.resumen_evaluacion.total_respuestas.si,
            data.resumen_evaluacion.total_respuestas.no,
          ],
          backgroundColor: ["#0066cc", "#ff9900"],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Porcentaje Global de Cumplimiento",
          font: {
            size: 16,
          },
        },
        legend: {
          position: "bottom",
        },
      },
    },
  });
}

// Función para crear el gráfico de barras
function crearGraficoBarras() {
  const ctx = document.getElementById("grafico-barras").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.resumen_evaluacion.procesos.map((p) => p.nombre),
      datasets: [
        {
          label: "% de Cumplimiento",
          data: data.resumen_evaluacion.procesos.map((p) => p.porcentaje),
          backgroundColor: "#0066cc",
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Cumplimiento por Proceso",
          font: {
            size: 16,
          },
        },
        legend: {
          display: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
        },
      },
    },
  });
}

// Función para generar el árbol de procesos
function generarArbolProcesos() {
  const arbolContainer = document.getElementById("arbol-procesos");
  data.procesos.forEach((proceso) => {
    const procesoElement = document.createElement("div");
    procesoElement.className = "proceso";
    procesoElement.innerHTML = `<span>${proceso.nombre} (${proceso.porcentaje_cumplimiento}%)</span>`;

    proceso.actividades.forEach((actividad) => {
      const actividadElement = document.createElement("div");
      actividadElement.className = "actividad";
      if (actividad.porcentaje_cumplimiento < 80) {
        actividadElement.classList.add("bajo-cumplimiento");
      }
      actividadElement.innerHTML = `<span>${actividad.nombre} (${actividad.porcentaje_cumplimiento}%)</span>`;

      actividad.tareas.forEach((tarea) => {
        const tareaElement = document.createElement("div");
        tareaElement.className = "tarea";
        if (tarea.porcentaje_cumplimiento < 80) {
          tareaElement.classList.add("bajo-cumplimiento");
        }
        tareaElement.innerHTML = `<span>${tarea.nombre} (${tarea.porcentaje_cumplimiento}%)</span>`;
        actividadElement.appendChild(tareaElement);
      });

      procesoElement.appendChild(actividadElement);
    });

    arbolContainer.appendChild(procesoElement);
  });
}

// Función para generar la tabla resumen
function generarTablaResumen() {
  const tbody = document.querySelector("#tabla-resumen table tbody");
  data.procesos.forEach((proceso) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
              <td>${proceso.nombre}</td>
              <td>${proceso.porcentaje_cumplimiento}%</td>
              <td>${proceso.preguntas_evaluadas}</td>
              <td>${proceso.preguntas_no_cumplidas}</td>
              <td>${proceso.recomendaciones.join("<br>")}</td>
          `;
    tbody.appendChild(tr);

    proceso.actividades.forEach((actividad) => {
      const trActividad = document.createElement("tr");
      trActividad.innerHTML = `
                  <td style="padding-left: 20px;">- ${actividad.nombre}</td>
                  <td>${actividad.porcentaje_cumplimiento}%</td>
                  <td colspan="3"></td>
              `;
      tbody.appendChild(trActividad);
    });
  });
}

// Inicializar todos los elementos del informe
document.addEventListener("DOMContentLoaded", () => {
  crearGraficoDona();
  crearGraficoBarras();
  generarArbolProcesos();
  generarTablaResumen();
});
