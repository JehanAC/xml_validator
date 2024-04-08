import tkinter as tk
from tkinter import filedialog, messagebox
from lxml import etree
import subprocess

def generate_schema(input_file, output_file, schema_type):
    try:
        if schema_type == 'DTD':
            command = ['java', '-jar', 'trang.jar', input_file, output_file + '.dtd']
        elif schema_type == 'XSD':
            command = ['java', '-jar', 'trang.jar', input_file, output_file + '.xsd']

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            message = f"{schema_type} schema generation successful."
        else:
            message = f"Error generating {schema_type} schema:\n{result.stderr}"

        messagebox.showinfo("Schema Generation", message)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_input_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def browse_output_file(output_entry, default_ext):
    file_path = filedialog.asksaveasfilename(defaultextension=default_ext)
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)

def validate_xml(xml_file, dtd_file, xsd_file):
    try:
        xml_tree = etree.parse(xml_file)
        error_messages = []

        # Validate against DTD
        if dtd_file:
            dtd = etree.DTD(open(dtd_file))
            is_valid_dtd = dtd.validate(xml_tree)
            if not is_valid_dtd:
                error_messages.append("XML is not valid against DTD.")

        # Validate against XSD
        if xsd_file:
            schema = etree.XMLSchema(file=xsd_file)
            is_valid_xsd = schema.validate(xml_tree)
            if not is_valid_xsd:
                error_messages.append("XML is not valid against XSD.")

        if error_messages:
            messagebox.showwarning("Validation Result", "\n".join(error_messages))
        else:
            # Display XML content without tags
            display_xml(xml_tree)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_xml(xml_tree):
    # Extract tag names and text content of XML nodes
    xml_content = "\n".join(f"{node.tag}: {node.text}" for node in xml_tree.iter() if node.text)
    messagebox.showinfo("XML Content", xml_content)


def create_gui():
    root = tk.Tk()
    root.title("XML Schema Generator and Validator")

    bg_color = "#f0f0f0"
    fg_color = "#333333"
    font = ("Arial", 10)

    root.configure(bg=bg_color)

    title_label = tk.Label(root, text="XML Schema Generator and Validator", bg=bg_color, fg=fg_color, font=("Arial", 14, "bold"))
    title_label.grid(row=0, column=0, columnspan=4, padx=5, pady=10)

    input_label = tk.Label(root, text="Input XML File:", bg=bg_color, fg=fg_color, font=font)
    input_label.grid(row=1, column=0, padx=5, pady=5)

    input_entry = tk.Entry(root, width=50)
    input_entry.grid(row=1, column=1, padx=5, pady=5)

    input_button = tk.Button(root, text="Browse", command=lambda: browse_input_file(input_entry), bg=bg_color, fg=fg_color, font=font)
    input_button.grid(row=1, column=2, padx=5, pady=5)

    dtd_output_label = tk.Label(root, text="DTD Output File:", bg=bg_color, fg=fg_color, font=font)
    dtd_output_label.grid(row=2, column=0, padx=5, pady=5)

    dtd_output_entry = tk.Entry(root, width=50)
    dtd_output_entry.grid(row=2, column=1, padx=5, pady=5)

    dtd_output_button = tk.Button(root, text="Browse", command=lambda: browse_output_file(dtd_output_entry, ".dtd"), bg=bg_color, fg=fg_color, font=font)
    dtd_output_button.grid(row=2, column=2, padx=5, pady=5)

    dtd_generate_button = tk.Button(root, text="Generate DTD", command=lambda: generate_schema(input_entry.get(), dtd_output_entry.get(), "DTD"), bg=bg_color, fg=fg_color, font=font)
    dtd_generate_button.grid(row=2, column=3, padx=5, pady=5)

    xsd_output_label = tk.Label(root, text="XSD Output File:", bg=bg_color, fg=fg_color, font=font)
    xsd_output_label.grid(row=3, column=0, padx=5, pady=5)

    xsd_output_entry = tk.Entry(root, width=50)
    xsd_output_entry.grid(row=3, column=1, padx=5, pady=5)

    xsd_output_button = tk.Button(root, text="Browse", command=lambda: browse_output_file(xsd_output_entry, ".xsd"), bg=bg_color, fg=fg_color, font=font)
    xsd_output_button.grid(row=3, column=2, padx=5, pady=5)

    xsd_generate_button = tk.Button(root, text="Generate XSD", command=lambda: generate_schema(input_entry.get(), xsd_output_entry.get(), "XSD"), bg=bg_color, fg=fg_color, font=font)
    xsd_generate_button.grid(row=3, column=3, padx=5, pady=5)

    validate_button = tk.Button(root, text="Validate XML", command=lambda: validate_xml(input_entry.get(), dtd_output_entry.get(), xsd_output_entry.get()), bg=bg_color, fg=fg_color, font=font)
    validate_button.grid(row=4, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
