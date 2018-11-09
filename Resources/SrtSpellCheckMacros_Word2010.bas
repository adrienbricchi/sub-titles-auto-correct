Attribute VB_Name = "SrtSpellCheckMacros"

Sub SrtSpellCheck()
   Options.AllowAccentedUppercase = True
   Options.IgnoreUppercase = False
   Application.Dialogs(wdDialogToolsSpellingAndGrammar).Show
   Application.Quit SaveChanges:=True
End Sub

Sub SrtFrSpellCheck()
   Options.AllowAccentedUppercase = True
   Options.IgnoreUppercase = False
   ActiveDocument.Range.LanguageID = wdFrench
   Application.Dialogs(wdDialogToolsSpellingAndGrammar).Show
   Application.Quit SaveChanges:=True
End Sub

Sub SrtEngSpellCheck()
   Options.IgnoreUppercase = False
   ActiveDocument.Range.LanguageID = wdEnglishUS
   Application.Dialogs(wdDialogToolsSpellingAndGrammar).Show
   Application.Quit SaveChanges:=True
End Sub
