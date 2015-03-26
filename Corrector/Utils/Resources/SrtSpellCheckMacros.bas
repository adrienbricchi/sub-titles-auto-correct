Attribute VB_Name = "SrtSpellCheckMacros"

Sub SrtSpellCheck()
   Application.Dialogs(wdDialogToolsSpellingAndGrammar).Show
   Application.Quit SaveChanges:=True
End Sub

Sub SrtFrSpellCheck()
   ActiveDocument.Range.LanguageID = wdFrench
   Application.Dialogs(wdDialogToolsSpellingAndGrammar).Show
   Application.Quit SaveChanges:=True
End Sub

Sub SrtEngSpellCheck()
   ActiveDocument.Range.LanguageID = wdEnglishUS
   Application.Dialogs(wdDialogToolsSpellingAndGrammar).Show
   Application.Quit SaveChanges:=True
End Sub
