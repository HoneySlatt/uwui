const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  clicked: () => ipcRenderer.invoke('clicked')
})
