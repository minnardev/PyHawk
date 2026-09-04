const vscode = require('vscode');
const path = require('path');

function getHawkTerminal() {
    let terminal = vscode.window.terminals.find(t => t.name === 'Hawk');
    if (!terminal) {
        terminal = vscode.window.createTerminal({
            name: 'Hawk',
            iconPath: new vscode.ThemeIcon('symbol-event')
        });
    }
    return terminal;
}

function activate(context) {
    let runDisposable = vscode.commands.registerCommand('hawk.runFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('Hawk: Нет открытого файла для запуска.');
            return;
        }

        if (editor.document.isDirty) {
            await editor.document.save();
        }

        const filePath = editor.document.fileName;
        const terminal = getHawkTerminal();
        terminal.show(false);
        terminal.sendText(`hawk run "${filePath}"`);
    });

    let buildDisposable = vscode.commands.registerCommand('hawk.buildFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('Hawk: Нет открытого файла для компиляции.');
            return;
        }

        if (editor.document.isDirty) {
            await editor.document.save();
        }

        const filePath = editor.document.fileName;
        const dir = path.dirname(filePath);
        const nameWithoutExt = path.basename(filePath, path.extname(filePath));
        const outBin = path.join(dir, nameWithoutExt);

        const terminal = getHawkTerminal();
        terminal.show(false);
        terminal.sendText(`hawk build "${filePath}" && "${outBin}"`);
    });

    let replDisposable = vscode.commands.registerCommand('hawk.openRepl', () => {
        const terminal = getHawkTerminal();
        terminal.show(false);
        terminal.sendText('hawk repl');
    });

    context.subscriptions.push(runDisposable, buildDisposable, replDisposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
