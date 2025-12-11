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

## Author

-   rogmoreno