REM  *****  BASIC  *****

Sub SrtEngSpellCheck

dim document   as object
dim dispatcher as object
document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim args1(0) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Language"
args1(0).Value = "Default_Anglais (U.S.A.)"

REM dispatcher.executeDispatch(document, ".uno:LanguageStatus", "", 0, args1())
dispatcher.execute(document, ".uno:SpellingAndGrammarDialog", "", 0, Array())
ThisComponent.store()
ThisComponent.close(True)

End Sub


sub SrtFrSpellCheck

dim document   as object
dim dispatcher as object
document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim args1(0) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Language"
args1(0).Value = "Default_Français (France)"

REM dispatcher.executeDispatch(document, ".uno:LanguageStatus", "", 0, args1())
dispatcher.execute(document, ".uno:SpellingAndGrammarDialog", "", 0, Array())
ThisComponent.store()
ThisComponent.close(True)

end sub
