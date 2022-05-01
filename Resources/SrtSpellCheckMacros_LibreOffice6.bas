REM  *****  BASIC  *****


Sub SrtEngSpellCheck

dim document   as object
dim dispatcher as object

document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim args1(0) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Language"
args1(0).Value = "Default_Anglais (U.S.A.)"

dispatcher.executeDispatch(document, ".uno:LanguageStatus", "", 0, args1())
Wait 500
dispatcher.executeDispatch(document, ".uno:SpellingAndGrammarDialog", "", 0, Array())

REM ThisComponent.store()
REM ThisComponent.close(True)

End Sub



sub SrtFrSpellCheck

dim document   as object
dim dispatcher as object

document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim args1(0) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Language"
args1(0).Value = "Default_Français (France)"

dispatcher.executeDispatch(document, ".uno:LanguageStatus", "", 0, args1())
Wait 500
dispatcher.executeDispatch(document, ".uno:SpellingAndGrammarDialog", "", 0, Array())

REM ThisComponent.store()
REM ThisComponent.close(True)

end sub


