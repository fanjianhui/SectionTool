# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.propgrid as pg

###########################################################################
## Class SectionPointDefsPanelBase
###########################################################################

class SectionPointDefsPanelBase ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 298,822 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"输入点坐标：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"X:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer4.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.m_textCtrl8 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 65,25 ), 0 )
		bSizer4.Add( self.m_textCtrl8, 0, wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Y:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer4.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		self.m_textCtrl9 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 65,25 ), 0 )
		bSizer4.Add( self.m_textCtrl9, 0, wx.ALL, 5 )
		
		self.m_button1 = wx.Button( self, wx.ID_ANY, u"Insert", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button1, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		bSizer50 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer51 = wx.BoxSizer( wx.VERTICAL )
		
		m_listBox2Choices = []
		self.m_listBox2 = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,150 ), m_listBox2Choices, 0 )
		bSizer51.Add( self.m_listBox2, 0, wx.ALL, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button7 = wx.Button( self, wx.ID_ANY, u"Add连通域", wx.DefaultPosition, wx.Size( 65,30 ), 0 )
		bSizer8.Add( self.m_button7, 0, wx.ALL, 5 )
		
		self.m_button5 = wx.Button( self, wx.ID_ANY, u"生成复连通", wx.DefaultPosition, wx.Size( 60,30 ), 0 )
		bSizer8.Add( self.m_button5, 0, wx.ALL, 5 )
		
		
		bSizer51.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		
		bSizer50.Add( bSizer51, 1, wx.EXPAND, 5 )
		
		bSizer52 = wx.BoxSizer( wx.VERTICAL )
		
		m_listBox3Choices = []
		self.m_listBox3 = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,150 ), m_listBox3Choices, 0 )
		bSizer52.Add( self.m_listBox3, 0, wx.ALL, 5 )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button8 = wx.Button( self, wx.ID_ANY, u"生成组合截面", wx.DefaultPosition, wx.Size( 75,30 ), 0 )
		bSizer10.Add( self.m_button8, 0, wx.ALL, 5 )
		
		self.m_button10 = wx.Button( self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button10, 0, wx.ALL, 5 )
		
		
		bSizer52.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		
		bSizer50.Add( bSizer52, 1, wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer50, 0, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,300 ), wx.TAB_TRAVERSAL )
		self.m_panel1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		
		bSizer7.Add( self.m_panel1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_button11 = wx.Button( self, wx.ID_ANY, u"输出数据文件", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button11, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		self.m_propertyGrid_result = pg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 330,320 ), wx.propgrid.PG_DEFAULT_STYLE)
		self.m_propertyGridItem1 = self.m_propertyGrid_result.Append( pg.PropertyCategory( u"结果数据", u"结果数据" ) ) 
		self.m_propertyGridItem2 = self.m_propertyGrid_result.Append( pg.StringProperty( u"面积          =", u"面积          =" ) ) 
		self.m_propertyGridItem3 = self.m_propertyGrid_result.Append( pg.StringProperty( u"Sx     ", u"Sx     " ) ) 
		self.m_propertyGridItem42 = self.m_propertyGrid_result.Append( pg.StringProperty( u"Sy", u"Sy" ) ) 
		self.m_propertyGridItem4 = self.m_propertyGrid_result.Append( pg.StringProperty( u"Ix", u"Ix" ) ) 
		self.m_propertyGridItem5 = self.m_propertyGrid_result.Append( pg.StringProperty( u"Iy", u"Iy" ) ) 
		self.m_propertyGridItem7 = self.m_propertyGrid_result.Append( pg.StringProperty( u"Ixy", u"Ixy" ) ) 
		self.m_propertyGridItem8 = self.m_propertyGrid_result.Append( pg.StringProperty( u"型心", u"型心" ) ) 
		self.m_propertyGridItem9 = self.m_propertyGrid_result.Append( pg.StringProperty( u"主惯性角", u"主惯性角" ) ) 
		self.m_propertyGridItem61 = self.m_propertyGrid_result.Append( pg.StringProperty( u"ix", u"ix" ) ) 
		self.m_propertyGridItem62 = self.m_propertyGrid_result.Append( pg.StringProperty( u"iy      ", u"iy      " ) ) 
		bSizer2.Add( self.m_propertyGrid_result, 1, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button1.Bind( wx.EVT_BUTTON, self.m_btn_InsertOnButtonClick )
		self.m_listBox2.Bind( wx.EVT_RIGHT_UP, self.del_OnRightClick )
		self.m_button7.Bind( wx.EVT_BUTTON, self.btn_addMultiPropOnButtonClick )
		self.m_button5.Bind( wx.EVT_BUTTON, self.btn_genMultiPropOnButtonClick )
		self.m_listBox3.Bind( wx.EVT_LEFT_DCLICK, self.showItemOnDClick )
		self.m_button8.Bind( wx.EVT_BUTTON, self.btn_genCompOnButtonClick )
		self.m_button10.Bind( wx.EVT_BUTTON, self.btn_DataClearOnClickButton )
		self.m_button11.Bind( wx.EVT_BUTTON, self.btn_PrintDataOnclick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_btn_InsertOnButtonClick( self, event ):
		event.Skip()
	
	def del_OnRightClick( self, event ):
		event.Skip()
	
	def btn_addMultiPropOnButtonClick( self, event ):
		event.Skip()
	
	def btn_genMultiPropOnButtonClick( self, event ):
		event.Skip()
	
	def showItemOnDClick( self, event ):
		event.Skip()
	
	def btn_genCompOnButtonClick( self, event ):
		event.Skip()
	
	def btn_DataClearOnClickButton( self, event ):
		event.Skip()
	
	def btn_PrintDataOnclick( self, event ):
		event.Skip()
	

