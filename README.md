# Plugin Flatpak Runner para StreamController

Un plugin para StreamController que permite listar y ejecutar aplicaciones Flatpak con un solo botón.

## Características

-   Añade una nueva acción **"Run Flatpak App"** a StreamController.
-   Detecta y lista automáticamente todas las aplicaciones instaladas vía Flatpak en un menú desplegable durante la configuración.
-   Ejecuta la aplicación seleccionada al presionar el botón en el deck.
-   Compatible con instalaciones de StreamController que se ejecutan de forma nativa o dentro de otro Flatpak.

## Instalación

1.  Asegúrate de que la carpeta `flatpak_run` se encuentre dentro del directorio de plugins de tu instalación de StreamController.
2.  Reinicia la aplicación de StreamController para que cargue el plugin.

## Uso

1.  En la interfaz de StreamController, arrastra la acción **"Run Flatpak App"** a un botón vacío.
2.  Aparecerá el diálogo de configuración. En el menú desplegable **"Application"**, selecciona la aplicación que deseas ejecutar.
3.  ¡Listo! Cierra la configuración. Al presionar el botón en tu deck, se lanzará la aplicación seleccionada.

## ¡Importante! Si usas StreamController como Flatpak

Para que este plugin pueda ver y ejecutar otras aplicaciones Flatpak de tu sistema, necesita que le concedas un permiso especial al Flatpak de StreamController.

Sigue estos pasos en una terminal de tu sistema:

1.  **Busca el ID de tu aplicación** de StreamController:
    ```bash
    flatpak list
    ```
    (El ID será algo como `com.core447.StreamController`)

2.  **Aplica el permiso** usando el ID que encontraste. Reemplaza `EL_ID_DE_STREAMCONTROLLER` con tu ID:
    ```bash
    flatpak override --user --talk-name=org.freedesktop.Flatpak EL_ID_DE_STREAMCONTROLLER
    ```

3.  **Reinicia StreamController** después de aplicar el permiso.

## Estructura del Código y Adaptación

El código del plugin se encuentra en el archivo `flatpak_run.py` y está escrito en Python. Ha sido diseñado con una estructura genérica de plugin, la cual puede necesitar ajustes para integrarse con la API específica de StreamController.

-   **`flatpak_run.py`**: Contiene toda la lógica del plugin.
    -   **`FlatpakRunPlugin`**: La clase principal del plugin, responsable de registrar la nueva acción en StreamController.
    -   **`RunFlatpakAppAction`**: La clase que define la acción "Run Flatpak App". Contiene la lógica para:
        -   Generar el menú de configuración con la lista de aplicaciones (`get_config_fields`).
        -   Ejecutar la aplicación seleccionada (`execute`).
    -   **`get_flatpak_apps()`**: Una función de utilidad que obtiene la lista de aplicaciones Flatpak instaladas en el sistema.

### Adaptación a la API de StreamController

El código asume la existencia de una API de StreamController con ciertas características. Si el plugin не funciona directamente, es probable que necesites ajustar las siguientes partes en `flatpak_run.py`:

1.  **Clase Base de la Acción**: `RunFlatpakAppAction` hereda de una clase hipotética `ActionBase`. Deberás cambiarla por la clase base que StreamController proporcione para las acciones.
2.  **Método de Registro**: El método `register(self, api)` asume que el objeto `api` tiene un método `register_action`. El nombre de este método y sus parámetros pueden ser diferentes.
3.  **Definición de la Configuración**: El método `get_config_fields` devuelve una estructura de datos para crear un menú desplegable. El formato (tipos de campo, IDs, etc.) debe coincidir con lo que espera la API de StreamController para construir interfaces de configuración.

## Autor

-   rogmoreno

---

# Flatpak Runner Plugin for StreamController

A plugin for StreamController that allows listing and running Flatpak applications with a single button.

## Features

-   Adds a new **"Run Flatpak App"** action to StreamController.
-   Automatically detects and lists all applications installed via Flatpak in a dropdown menu during configuration.
-   Runs the selected application when the button on the deck is pressed.
-   Compatible with StreamController installations running natively or inside another Flatpak.

## Installation

1.  Ensure the `flatpak_run` folder is inside the plugins directory of your StreamController installation.
2.  Restart the StreamController application to load the plugin.

## Usage

1.  In the StreamController interface, drag the **"Run Flatpak App"** action to an empty button.
2.  The configuration dialog will appear. In the **"Application"** dropdown menu, select the application you want to run.
3.  Done! Closing the configuration. Pressing the button on your deck will now launch the selected application.

## Important! If you use StreamController as a Flatpak

For this plugin to be able to see and run other Flatpak applications on your system, you need to grant a special permission to the StreamController Flatpak.

Follow these steps in your system's terminal:

1.  **Find your StreamController application ID**:
    ```bash
    flatpak list
    ```
    (The ID will be something like `com.core447.StreamController`)

2.  **Apply the permission** using the ID you found. Replace `YOUR_STREAMCONTROLLER_ID` with your ID:
    ```bash
    flatpak override --user --talk-name=org.freedesktop.Flatpak YOUR_STREAMCONTROLLER_ID
    ```

3.  **Restart StreamController** after applying the permission.

## Code Structure and Adaptation

The plugin's code is located in the `flatpak_run.py` file and is written in Python. It has been designed with a generic plugin structure, which may require adjustments to integrate with the specific StreamController API.

-   **`flatpak_run.py`**: Contains all the plugin's logic.
    -   **`FlatpakRunPlugin`**: The main plugin class, responsible for registering the new action with StreamController.
    -   **`RunFlatpakAppAction`**: The class that defines the "Run Flatpak App" action. It contains the logic to:
        -   Generate the configuration menu with the list of applications (`get_config_fields`).
        -   Execute the selected application (`execute`).
    -   **`get_flatpak_apps()`**: A utility function that retrieves the list of Flatpak applications installed on the system.

### Adapting to the StreamController API

The code assumes the existence of a StreamController API with certain features. If the plugin does not work out-of-the-box, you will likely need to adjust the following parts in `flatpak_run.py`:

1.  **Action Base Class**: `RunFlatpakAppAction` inherits from a hypothetical `ActionBase` class. You should change it to the base class provided by StreamController for actions.
2.  **Registration Method**: The `register(self, api)` method assumes that the `api` object has a `register_action` method. The name of this method and its parameters may be different.
3.  **Configuration Definition**: The `get_config_fields` method returns a data structure to create a dropdown menu. The format (field types, IDs, etc.) must match what the StreamController API expects for building configuration interfaces.

## Autor

-   rogmoreno