#!/usr/bin/python3
# -*-coding:utf8 -*

"""
Minimal tkinter GUI interface for subtitle corrections.
Provides buttons for each type of correction that can be applied.
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os

from subtitles_auto_correct.models.subtitle import Subtitle
from subtitles_auto_correct.utils.file_utils import get_file_text, write_file, get_file_language
from subtitles_auto_correct.utils.strings_utils import (
    # Single-line corrections
    fix_accentuated_capital_a,
    fix_capital_i_to_l,
    fix_capital_v_to_v,
    fix_zero_to_o,
    fix_l_to_capital_i,
    fix_punctuation_errors,
    fix_punctuation_spaces,
    fix_dialog_hyphen,
    fix_degree_symbol,
    fix_colon,
    fix_quotes,
    fix_italic_tag_errors,
    fix_common_errors,
    fix_numbers,
    fix_acronyms,
    fix_common_misspells,
    # Multi-line corrections
    fix_3d_doubles,
    fix_empty_lines,
    fix_redundant_italic_tag,
    fix_useless_dialog_hyphen,
    fix_missing_dialog_hyphen,
    fix_double_quotes_errors,
    fix_sdh_tags,
    # Aggregate corrections
    fix_single_line_errors,
    fix_multi_line_errors,
    # External spell checkers
    launch_ms_word_spell_check,
    launch_libreoffice_6_writer_spell_check,
)


class SubtitleCorrectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Subtitle Auto Corrector")
        self.current_file = None
        self.current_language = None

        # Create UI
        self.create_ui()

    def create_ui(self):
        """Create the minimal GUI interface."""
        # File selection section
        file_frame = tk.Frame(self.root, padx=10, pady=10)
        file_frame.pack(fill=tk.X)

        tk.Label(file_frame, text="File:").pack(side=tk.LEFT)
        self.file_label = tk.Label(file_frame, text="No file selected", fg="gray")
        self.file_label.pack(side=tk.LEFT, padx=10)

        tk.Button(file_frame, text="Select .srt File", command=self.select_file).pack(side=tk.RIGHT)

        # Create a scrollable frame for all buttons
        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Main corrections frame
        main_frame = tk.Frame(scrollable_frame, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # AGGREGATE CORRECTIONS (most commonly used)
        self.create_section(main_frame, "🔧 QUICK CORRECTIONS", [
            ("All Single-Line Corrections", self.apply_all_single_line),
            ("All Multi-Line Corrections", self.apply_all_multi_line),
            ("All Corrections (Single + Multi)", self.apply_all_corrections),
        ])

        # SINGLE-LINE CORRECTIONS - Character Fixes
        self.create_section(main_frame, "📝 Character Fixes", [
            ("Fix À (Accentuated A)", self.apply_accentuated_capital_a),
            ("Fix I → l (capital I to lowercase L)", self.apply_capital_i_to_l),
            ("Fix V → v (capital V to lowercase)", self.apply_capital_v_to_v),
            ("Fix 0 → o (zero to letter O)", self.apply_zero_to_o),
            ("Fix l → I (lowercase L to capital I)", self.apply_l_to_capital_i),
        ])

        # SINGLE-LINE CORRECTIONS - Punctuation
        self.create_section(main_frame, "🔤 Punctuation Fixes", [
            ("Fix Punctuation Errors (... dots, dashes)", self.apply_punctuation_errors),
            ("Fix Punctuation Spaces (?, !)", self.apply_punctuation_spaces),
            ("Fix Dialog Hyphens (- spacing)", self.apply_dialog_hyphen),
            ("Fix Degree Symbol (°)", self.apply_degree_symbol),
            ("Fix Colons (:)", self.apply_colon),
            ("Fix Quotes (\" and ')", self.apply_quotes),
        ])

        # SINGLE-LINE CORRECTIONS - Formatting
        self.create_section(main_frame, "🎨 Format Fixes", [
            ("Fix Italic Tags (<i></i>)", self.apply_italic_tag_errors),
            ("Fix Common Errors (unicode quotes, dashes)", self.apply_common_errors),
            ("Fix Numbers (spacing, formatting)", self.apply_numbers),
            ("Fix Acronyms (U.S. A → U.S.A)", self.apply_acronyms),
            ("Fix Common Misspells (from CSV)", self.apply_common_misspells),
        ])

        # MULTI-LINE CORRECTIONS
        self.create_section(main_frame, "📋 Multi-Line Fixes", [
            ("Remove 3D Duplicates", self.apply_3d_doubles),
            ("Remove Empty Lines", self.apply_empty_lines),
            ("Remove Redundant Italic Tags", self.apply_redundant_italic_tag),
            ("Remove Useless Dialog Hyphens", self.apply_useless_dialog_hyphen),
            ("Add Missing Dialog Hyphens", self.apply_missing_dialog_hyphen),
            ("Fix Double Quote Balance", self.apply_double_quotes_errors),
            ("Remove SDH Tags ([SOUND], ♪, etc.)", self.apply_sdh_tags),
        ])

        # EXTERNAL SPELL CHECKERS
        self.create_section(main_frame, "🔍 External Spell Checkers", [
            ("MS Word Spell Check", self.apply_ms_word_spell_check),
            ("LibreOffice Writer Spell Check", self.apply_libreoffice_spell_check),
        ])

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def create_section(self, parent, title, buttons):
        """Create a section with a title and buttons."""
        frame = tk.LabelFrame(parent, text=title, padx=10, pady=5)
        frame.pack(fill=tk.X, pady=5)

        for text, command in buttons:
            tk.Button(frame, text=text, command=command, width=50, anchor=tk.W).pack(fill=tk.X, pady=2)

    def select_file(self):
        """Select a .srt subtitle file."""
        filename = filedialog.askopenfilename(
            title="Select Subtitle File",
            filetypes=[("SRT files", "*.srt"), ("All files", "*.*")]
        )

        if filename:
            self.current_file = filename
            self.current_language = get_file_language(filename)
            self.file_label.config(text=os.path.basename(filename), fg="black")
            self.status_label.config(text=f"Loaded: {filename} (Language: {self.current_language})")

    def check_file_selected(self):
        """Check if a file is selected."""
        if not self.current_file:
            messagebox.showerror("Error", "Please select a .srt file first!")
            return False
        return True

    def apply_correction(self, correction_name, correction_func, is_multi_line=False, needs_language=False):
        """Apply a correction function to the current file."""
        if not self.check_file_selected():
            return

        try:
            self.status_label.config(text=f"Applying {correction_name}...")
            self.root.update()

            # Read file
            lines = get_file_text(self.current_file, True)

            if is_multi_line:
                # Multi-line correction (works on subtitle blocks)
                subtitles = Subtitle.subtitles_from_lines(lines)

                for subtitle in subtitles:
                    corrected_lines = correction_func(subtitle.lines)
                    subtitle.set_lines(corrected_lines)

                # Save file
                new_lines = []
                for subtitle in subtitles:
                    if len(subtitle.lines) > 0:
                        new_lines += subtitle.to_lines()
                        new_lines.append("\n")

                write_file(self.current_file, new_lines)
            else:
                # Single-line correction
                subtitles = Subtitle.subtitles_from_lines(lines)

                for subtitle in subtitles:
                    corrected_lines = []
                    for line in subtitle.get_lines():
                        if needs_language:
                            line = correction_func(line, self.current_language)
                        else:
                            line = correction_func(line)
                        corrected_lines.append(line)
                    subtitle.set_lines(corrected_lines)

                # Save file
                new_lines = []
                for subtitle in subtitles:
                    if len(subtitle.lines) > 0:
                        new_lines += subtitle.to_lines()
                        new_lines.append("\n")

                write_file(self.current_file, new_lines)

            self.status_label.config(text=f"✓ {correction_name} applied successfully!")
            messagebox.showinfo("Success", f"{correction_name} has been applied!")

        except Exception as e:
            self.status_label.config(text=f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to apply correction:\n{str(e)}")

    # Single-line corrections
    def apply_accentuated_capital_a(self):
        self.apply_correction("Fix À", fix_accentuated_capital_a)

    def apply_capital_i_to_l(self):
        self.apply_correction("Fix I → l", fix_capital_i_to_l, needs_language=True)

    def apply_capital_v_to_v(self):
        self.apply_correction("Fix V → v", fix_capital_v_to_v, needs_language=True)

    def apply_zero_to_o(self):
        self.apply_correction("Fix 0 → o", fix_zero_to_o)

    def apply_l_to_capital_i(self):
        self.apply_correction("Fix l → I", fix_l_to_capital_i)

    def apply_punctuation_errors(self):
        self.apply_correction("Fix Punctuation Errors", fix_punctuation_errors)

    def apply_punctuation_spaces(self):
        self.apply_correction("Fix Punctuation Spaces", fix_punctuation_spaces, needs_language=True)

    def apply_dialog_hyphen(self):
        self.apply_correction("Fix Dialog Hyphens", fix_dialog_hyphen)

    def apply_degree_symbol(self):
        self.apply_correction("Fix Degree Symbol", fix_degree_symbol)

    def apply_colon(self):
        self.apply_correction("Fix Colons", fix_colon, needs_language=True)

    def apply_quotes(self):
        self.apply_correction("Fix Quotes", fix_quotes, needs_language=True)

    def apply_italic_tag_errors(self):
        self.apply_correction("Fix Italic Tags", fix_italic_tag_errors)

    def apply_common_errors(self):
        self.apply_correction("Fix Common Errors", fix_common_errors)

    def apply_numbers(self):
        self.apply_correction("Fix Numbers", fix_numbers, needs_language=True)

    def apply_acronyms(self):
        self.apply_correction("Fix Acronyms", fix_acronyms)

    def apply_common_misspells(self):
        self.apply_correction("Fix Common Misspells", fix_common_misspells, needs_language=True)

    # Multi-line corrections
    def apply_3d_doubles(self):
        self.apply_correction("Remove 3D Duplicates", fix_3d_doubles, is_multi_line=True)

    def apply_empty_lines(self):
        self.apply_correction("Remove Empty Lines", fix_empty_lines, is_multi_line=True)

    def apply_redundant_italic_tag(self):
        self.apply_correction("Remove Redundant Italic Tags", fix_redundant_italic_tag, is_multi_line=True)

    def apply_useless_dialog_hyphen(self):
        self.apply_correction("Remove Useless Dialog Hyphens", fix_useless_dialog_hyphen, is_multi_line=True)

    def apply_missing_dialog_hyphen(self):
        self.apply_correction("Add Missing Dialog Hyphens", fix_missing_dialog_hyphen, is_multi_line=True)

    def apply_double_quotes_errors(self):
        self.apply_correction("Fix Double Quote Balance", fix_double_quotes_errors, is_multi_line=True)

    def apply_sdh_tags(self):
        self.apply_correction("Remove SDH Tags", fix_sdh_tags, is_multi_line=True)

    # Aggregate corrections
    def apply_all_single_line(self):
        """Apply all single-line corrections."""
        if not self.check_file_selected():
            return

        try:
            self.status_label.config(text="Applying all single-line corrections...")
            self.root.update()

            lines = get_file_text(self.current_file, True)
            subtitles = Subtitle.subtitles_from_lines(lines)

            for subtitle in subtitles:
                corrected_lines = []
                for line in subtitle.get_lines():
                    line = fix_single_line_errors(line, self.current_language)
                    corrected_lines.append(line)
                subtitle.set_lines(corrected_lines)

            # Save file
            new_lines = []
            for subtitle in subtitles:
                if len(subtitle.lines) > 0:
                    new_lines += subtitle.to_lines()
                    new_lines.append("\n")

            write_file(self.current_file, new_lines)

            self.status_label.config(text="✓ All single-line corrections applied!")
            messagebox.showinfo("Success", "All single-line corrections have been applied!")

        except Exception as e:
            self.status_label.config(text=f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to apply corrections:\n{str(e)}")

    def apply_all_multi_line(self):
        """Apply all multi-line corrections."""
        if not self.check_file_selected():
            return

        try:
            self.status_label.config(text="Applying all multi-line corrections...")
            self.root.update()

            lines = get_file_text(self.current_file, True)
            subtitles = Subtitle.subtitles_from_lines(lines)

            for subtitle in subtitles:
                corrected_lines = fix_multi_line_errors(subtitle.lines)
                subtitle.set_lines(corrected_lines)

            # Save file
            new_lines = []
            for subtitle in subtitles:
                if len(subtitle.lines) > 0:
                    new_lines += subtitle.to_lines()
                    new_lines.append("\n")

            write_file(self.current_file, new_lines)

            self.status_label.config(text="✓ All multi-line corrections applied!")
            messagebox.showinfo("Success", "All multi-line corrections have been applied!")

        except Exception as e:
            self.status_label.config(text=f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to apply corrections:\n{str(e)}")

    def apply_all_corrections(self):
        """Apply all corrections (both single-line and multi-line)."""
        if not self.check_file_selected():
            return

        try:
            self.status_label.config(text="Applying all corrections...")
            self.root.update()

            lines = get_file_text(self.current_file, True)
            subtitles = Subtitle.subtitles_from_lines(lines)

            # Multi-line corrections first
            for subtitle in subtitles:
                corrected_lines = fix_multi_line_errors(subtitle.lines)
                subtitle.set_lines(corrected_lines)

            # Then single-line corrections
            for subtitle in subtitles:
                corrected_lines = []
                for line in subtitle.get_lines():
                    line = fix_single_line_errors(line, self.current_language)
                    corrected_lines.append(line)
                subtitle.set_lines(corrected_lines)

            # Save file
            new_lines = []
            for subtitle in subtitles:
                if len(subtitle.lines) > 0:
                    new_lines += subtitle.to_lines()
                    new_lines.append("\n")

            write_file(self.current_file, new_lines)

            self.status_label.config(text="✓ All corrections applied!")
            messagebox.showinfo("Success", "All corrections have been applied successfully!")

        except Exception as e:
            self.status_label.config(text=f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to apply corrections:\n{str(e)}")

    # External spell checkers
    def apply_ms_word_spell_check(self):
        """Launch MS Word spell check."""
        if not self.check_file_selected():
            return

        try:
            self.status_label.config(text="Launching MS Word spell check...")
            self.root.update()

            launch_ms_word_spell_check(self.current_file, self.current_language)

            self.status_label.config(text="✓ MS Word spell check completed!")
            messagebox.showinfo("Success", "MS Word spell check has been launched!")

        except Exception as e:
            self.status_label.config(text=f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to launch MS Word:\n{str(e)}")

    def apply_libreoffice_spell_check(self):
        """Launch LibreOffice Writer spell check."""
        if not self.check_file_selected():
            return

        try:
            self.status_label.config(text="Launching LibreOffice Writer spell check...")
            self.root.update()

            launch_libreoffice_6_writer_spell_check(self.current_file, self.current_language)

            self.status_label.config(text="✓ LibreOffice Writer spell check completed!")
            messagebox.showinfo("Success", "LibreOffice Writer spell check has been launched!")

        except Exception as e:
            self.status_label.config(text=f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to launch LibreOffice:\n{str(e)}")


def launch_gui():
    """Launch the GUI application."""
    root = tk.Tk()
    app = SubtitleCorrectorGUI(root)
    root.geometry("700x600")
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
